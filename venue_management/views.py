"""
views.py - Responsible for handling this application's views
"""

# Imports
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lo
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, PromoCodeForm
from .models import VenueManager, PromoCode, Venue, Location, Concert

def index(request):
    """
    The default index view for the Venue Management panel.
    :param request: (Django) object of the request's properties
    :return:
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')

    return render(request, 'venue_management/index.html')


def login_manager_window(request):
    """
    The login page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the login page
    """
    # Send the user to the panel if already authenticated as a VenueManager.
    if request.user.is_authenticated and isinstance(request.user, VenueManager):
        return redirect('/venue/panel')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email , password=password, model=VenueManager)

        if user is not None:
            login(request, user)
            return redirect('/venue/panel')

        error = 'Invalid username or password. Please try again.'
        print(error)
        return render(request, 'venue_management/login.html', {'messages': error})

    return render(request, 'venue_management/login.html')


def register_manager_window(request):
    """
    The registration page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the registration page
    """
    # Send the user to the panel if already authenticated as a VenueManager.
    if request.user.is_authenticated and isinstance(request.user, VenueManager):
        return redirect('/venue/panel')

    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password, model=VenueManager)

            login(request, user)
            return redirect('/venue/panel')
    else:
        form = RegisterForm()
    return render(request, 'venue_management/register.html', {'form': form})

@login_required(login_url='/venue/login')
def logout(request):
    """
    Logs the current user out
    :param request: (Django) object of the request's properties
    :return: redirects home
    """
    lo(request)
    return redirect('/venue')

@login_required(login_url='/venue/login')
def manage_venue(request, venue_id):
    """
    Management page for the given venue
    :param request: (Django) object of the request's properties
    :param venue_id: the ID of the venue to manage
    :return: venue management page
    """
    provinces = Location.Province.choices

    # Ensure the user has permission to do this
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the venue exists
        if Venue.objects.filter(pk=venue_id).exists():
            venue = Venue.objects.get(pk=venue_id)

            # Check if the user is a manager of the venue
            if venue.managers.contains(request.user):
                return render(request, 'venue_management/manage_venue.html', {
                    'venue': venue,
                    'provinces': provinces
                })

        # User doesn't have permission or the venue doesn't exist.
        return render(request, 'venue_management/panel.html', {
            "venues": venues,
            "error_message": "You do not have permission to manage this venue!"
        })
    return redirect('/venue/logout/')

@login_required(login_url='/venue/login')
def delete_venue(request, venue_id):
    """
    Deletes the specified venue
    :param venue_id: the ID of the venue to delete
    :param request: (Django) object of the request's properties
    :return: refreshes the page or gives an error
    """

    # Ensure the user has permission to do this
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the venue exists
        if Venue.objects.filter(pk=venue_id).exists():
            venue = Venue.objects.get(pk=venue_id)

            # Check if the user is a manager of the venue
            if venue.managers.contains(request.user):
                # User has all permissions. Delete the venue.
                venue.delete()
                return render(request, 'venue_management/panel.html', {
                    'success_message': "Successfully deleted the venue!",
                    'venues': venues,
                    'redirect': True
                })
            # The user isn't a manager of this venue
            return render(request, 'venue_management/panel.html', {
                'error_message': "You are not a manager of this venue!",
                'venues': venues,
                'redirect': True
            })
        # The venue doesn't exist
        return render(request, 'venue_management/panel.html', {
            'error_message': "This venue does not exist!",
            'venues': venues,
            'redirect': True
        })
    # User not logged in
    return redirect('/venue/logout')

@login_required(login_url='/venue/login')
def panel(request):
    """
    The home page for a signed in venue manager
    :param request: (Django) object of the request's properties
    :return: the venue manager's panel
    """
    venues = request.user.venues.all()
    provinces = Location.Province.choices

    if len(venues) == 0:
        venues = None

    return render(request, 'venue_management/panel.html', {'venues': venues, 'provinces': provinces})

@login_required(login_url='/venue/login')
def add_venue(request):
    """Adds a new venue to the database"""
    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # General Venue Information
        name = request.POST['name']
        description = request.POST['description']
        website = request.POST['website']
        image = request.FILES.get('venue_image')
        manager = request.user

        # Venue Location information
        street_num = request.POST['street_num']
        street_name = request.POST['street_name']
        city = request.POST['city']
        province = Location.Province(request.POST['province'])

        # Form Models and save to DB
        venue_location = Location(street_num=street_num, street_name=street_name, city=city, province=province)
        venue_location.save()
        venue = Venue(name=name, description=description, website=website, image=image, location=venue_location)
        venue.save()
        venue.managers.add(manager)
        return redirect('/venue/panel/')

    return render(request, 'venue_management/add_venue.html')

@login_required(login_url='/venue/login')
def edit_venue(request, venue_id):
    """
    Edits a venue in the database
    :param request: (Django) object of the request's properties
    :param venue_id: The venue ID to edit
    :returns: redirect to appropriate page
    """

    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # Check if the venue exists
        if Venue.objects.filter(pk=venue_id).exists():
            venue = Venue.objects.get(pk=venue_id)

            # Check if the user is a manager of the venue
            if venue.managers.contains(request.user):
                # User has all permissions. Edit the venue.

                # General Venue Information
                venue.name = request.POST['name']
                venue.description = request.POST['description']
                venue.website = request.POST['website']
                venue.image = request.FILES.get('venue_image')
                venue.save()

                # Venue Location information
                location = venue.location
                location.street_num = request.POST['street_num']
                location.street_name = request.POST['street_name']
                location.city = request.POST['city']
                location.province = Location.Province(request.POST['province'])
                location.save()

    return redirect(f'/venue/panel/{venue_id}/')

# @login_required
# @require_http_methods(["GET", "POST"])
def generate_promo_code(request):
    """
    TODO: What is this?
    :param request: (Django) object of the request's properties
    :return: the promo code page
    """
    if request.method == "POST":
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            # Generate Promo Code
            promo_code = PromoCode.objects.create(
                code=form.cleaned_data["discount"],
                discount=form.cleaned_data["discount"],
                expiration_date=form.cleaned_data["expiration_date"],
            )

            # Render promo code on the screen
            context = {
                "promo_code": promo_code.code,
            }
            promo_code_html = render_to_string(
                "venue_management/promo_code.html", context
            )
            return HttpResponse(promo_code_html)
    else:
        form = PromoCodeForm()
    return render(request, "venue_management/generate_promo_code.html", {"form": form})



def add_concert(request):
    """This view is used for adding new concert to the html and using POST request that concert is added to the
       database"""
    if request.method == 'POST':
        name = request.POST['name']
        artist_name = request.POST['artist_name']
        concert_date= request.POST['concert_date']
        min_age= request.POST['min_age']
        price = request.POST['price']
        concert_image = request.FILES.get('concert_image')
        description= request.POST['description']

        new_concert = Concert(name= name, artist_name=artist_name,concert_date=concert_date,min_age=min_age,price=
                              price,concert_image=concert_image,description=description)
        new_concert.save()
        return redirect('/venue/concerts/')

    return render(request, 'venue_management/Add_concert.html')

def buy(request, concert_id):
    """Buy concept based on the selected concert"""
    # Retrieve the selected concert using the concert_id parameter
    concert = Concert.objects.get(pk=concert_id)
    # Pass the concert data to the template
    context = {'concert': concert}
    return render(request, 'venue_management/buy.html', context)
