"""
views.py - Responsible for handling this application's views
"""

# Imports
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lo
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from ticketing.models import Eventgoer

from .forms import RegisterForm, PromoCodeForm
from .models import VenueManager, PromoCode, Venue, Location, Concert, SeatType, SeatRestriction


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
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password, model=VenueManager)

        # Ensure user exists and check if they are a venue manager
        if user is not None and isinstance(user, VenueManager):
            login(request, user)
            return redirect('/venue/panel')
        if isinstance(user, Eventgoer):
            # User is an eventgoer. Give an error message
            error = "The account you provided is an Eventgoer. Please log into the Client Site instead."
        else:
            # Invalid credentials provided.
            error = 'Invalid username or password. Please try again.'

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
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')

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
    return redirect('/venue/login')


@login_required(login_url='/venue/login')
def account(request):
    """
    Serves the Venue Manager's account details page and accepts updated form data.
    :param request: (Django) object of the request's properties
    :return: account details page
    """
    # Ensure the user is a venue manager
    if isinstance(request.user, VenueManager):
        # Check for a form submission
        if request.method == 'POST':
            # Process update form submission
            try:
                # Grab passwords from the form
                current_password = request.POST['password']
                if authenticate(request, email=request.user.email, password=current_password, model=VenueManager):
                    request.user.first_name = request.POST['first_name']
                    request.user.last_name = request.POST['last_name']
                    if 'new_password' in request.POST.keys() and request.POST['new_password'] is not None \
                            and request.POST['new_password'] != "":
                        # Set the new password, if provided in the form
                        request.user.set_password(request.POST['new_password'])

                    # Save the user's account
                    request.user.save()
                    # User account information updated
                    return render(request, 'venue_management/account.html', {
                        "success_message": "Successfully updated account data!"
                    })
                # Provided password was incorrect
                return render(request, 'venue_management/account.html', {
                    "error_message": "The password you gave was incorrect. Please try again."
                })
            except (NameError, KeyError):
                # Invalid information received
                return render(request, 'venue_management/account.html', {
                    "error_message": "Failed to update account data! Invalid form contents received."
                })
        # Serve account page
        return render(request, 'venue_management/account.html')

    return redirect('/venue/logout/')

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
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        provinces = Location.Province.choices

        if len(venues) == 0:
            venues = None

        return render(request, 'venue_management/panel.html', {'venues': venues, 'provinces': provinces})

    return redirect('/venue/logout/')


@login_required(login_url='/venue/login')
def add_venue(request):
    """
    Adds a venue to the database
    :param request: (Django) object of the request's properties
    :return: venue_management page
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

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
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

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
                image = request.FILES.get('venue_image')
                # Update the image if a new one is available
                if image is not None:
                    venue.image = image

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


@login_required(login_url='/venue/login/')
def add_concert(request, venue_id):
    """
    This view is used for adding new concert to the html and using POST request that concert is added to the database
   """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # Check if the venue exists
        if Venue.objects.filter(pk=venue_id).exists():
            venue = Venue.objects.get(pk=venue_id)

            # Check if the user is a manager of the venue
            if venue.managers.contains(request.user):
                # User has all permissions. Add the concert.

                # Gather concert information
                name = request.POST['name']
                artist_name = request.POST['artist_name']
                concert_date = request.POST['concert_date']
                min_age = request.POST['min_age']
                concert_image = request.FILES.get('concert_image')
                description = request.POST['description']

                # Create and save the new concert
                new_concert = Concert(name=name, artist_name=artist_name, concert_date=concert_date, min_age=min_age,
                                      concert_image=concert_image, description=description)
                new_concert.save()

                # Add the concert to the venue.
                venue.concerts.add(new_concert)
                return redirect(f'/venue/panel/{venue_id}')

    # Does not have permission to add here.
    return redirect('/venue/panel/')


@login_required(login_url='/venue/login')
def manage_concert(request, concert_id):
    """
    Management page for the given concert
    :param request: (Django) object of the request's properties
    :param concert_id: the ID of the concert to manage
    :return: concert management page
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    # Ensure the user has permission to do this
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the concert exists
        if Concert.objects.filter(pk=concert_id).exists():
            concert = Concert.objects.get(pk=concert_id)
            mapping = [restriction.seat_type.id for restriction in concert.restrictions.all()]

            # Check if the user is a manager of the venue that manages the concert
            if concert.venues.first().managers.contains(request.user):
                return render(request, 'venue_management/manage_concert.html', {
                    'concert': concert,
                    'mapping': mapping
                })

        # User doesn't have permission to the venue of this concert
        return render(request, 'venue_management/panel.html', {
            "venues": venues,
            "error_message": "You do not have permission to manage this concert!"
        })

    # The user may not be logged in as a valid Venue Manager.
    return redirect('/venue/logout/')


@login_required(login_url='/venue/login')
def edit_concert(request, concert_id):
    """
    Edits a concert in the database
    :param request: (Django) object of the request's properties
    :param concert_id: The concert ID to edit
    :returns: redirect to appropriate page
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # Check if the concert exists
        if Concert.objects.filter(pk=concert_id).exists():
            concert = Concert.objects.get(pk=concert_id)

            # Check if the user is a manager of the venue running the concert
            if concert.venues.first().managers.contains(request.user):
                # User has all permissions. Edit the concert.

                # Gather concert information and save it to the concert
                concert.name = request.POST['name']
                concert.artist_name = request.POST['artist_name']
                concert.concert_date = request.POST['concert_date']
                concert.min_age = request.POST['min_age']
                image = request.FILES.get('concert_image')
                # Update the image if a new one is available
                if image is not None:
                    concert.concert_image = image
                concert.description = request.POST['description']

                concert.save()

                return redirect(f'/venue/panel/concert/{concert_id}/')

    # Didn't successfully update (no perms)
    return redirect('/venue/panel/')


@login_required(login_url='/venue/login')
def delete_concert(request, concert_id):
    """
    Deletes the specified concert
    :param concert_id: the ID of the concert to delete
    :param request: (Django) object of the request's properties
    :return: refreshes the page or gives an error
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    # Ensure the user has permission to do this
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the venue exists
        if Concert.objects.filter(pk=concert_id).exists():
            concert = Concert.objects.get(pk=concert_id)

            # Check if the user is a manager of the concert
            if concert.venues.first().managers.contains(request.user):
                venue = concert.venues.first()
                # User has all permissions. Delete the concert.
                concert.delete()
                return render(request, 'venue_management/manage_venue.html', {
                    'success_message': "Successfully deleted the concert!",
                    'venue': venue,
                    'redirect': True
                })
            # The user isn't a manager of the venue that manages this concert
            return render(request, 'venue_management/panel.html', {
                'error_message': "You are not a manager of the venue that controls this concert!",
                'venues': venues,
                'redirect': True
            })
        # The concert doesn't exist
        return render(request, 'venue_management/panel.html', {
            'error_message': "This concert does not exist!",
            'venues': venues,
            'redirect': True
        })
    # User not logged in
    return redirect('/venue/logout')


@login_required(login_url='/venue/login/')
def add_seat(request, venue_id):
    """
    Adds a seat type to the venue in the database
    :param request: (Django) object of the request's properties
    :param venue_id: The ID of the venue to add it to
    :returns: redirect to appropriate page
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # Check if the venue exists
        if Venue.objects.filter(pk=venue_id).exists():
            venue = Venue.objects.get(pk=venue_id)

            # Check if the user is a manager of the venue
            if venue.managers.contains(request.user):
                # User has all permissions. Add the concert.

                # Gather seat type information
                name = request.POST['name']
                quantity = request.POST['quantity']
                price = request.POST['price']

                # Create and save the new seat type
                new_seat = SeatType(name=name, quantity=quantity, price=price)
                new_seat.save()

                # Add the seat type to the venue.
                venue.seat_types.add(new_seat)
                return redirect(f'/venue/panel/{venue_id}')

    # Does not have permission to add here.
    return redirect('/venue/panel/')


@login_required(login_url='/venue/login')
def edit_seat(request, seat_id):
    """
    Edits a seat type in the database
    :param request: (Django) object of the request's properties
    :param seat_id: The seat type ID to edit
    :returns: redirect to appropriate page
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    if request.method == 'POST' and isinstance(request.user, VenueManager):
        # Check if the seat type exists
        if SeatType.objects.filter(pk=seat_id).exists():
            seat_type = SeatType.objects.get(pk=seat_id)
            venue = seat_type.venues.first()

            # Check if the user is a manager of the venue
            if seat_type.venues.first().managers.contains(request.user):
                # User has all permissions. Edit the concert.

                # Gather concert information and save it to the concert
                seat_type.name = request.POST['name']
                seat_type.quantity = request.POST['quantity']
                seat_type.price = request.POST['price']
                seat_type.save()

                return redirect(f'/venue/panel/{venue.id}/')

    # Didn't successfully update (no perms)
    return redirect('/venue/panel/')


@login_required(login_url='/venue/login')
def delete_seat(request, seat_id):
    """
    Deletes the specified seat type
    :param seat_id: the ID of the seat type to delete
    :param request: (Django) object of the request's properties
    :return: refreshes the page or gives an error
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    # Ensure the user has permission to do this
    if isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the venue exists
        if SeatType.objects.filter(pk=seat_id).exists():
            seat_type = SeatType.objects.get(pk=seat_id)

            # Check if the user is a manager of the seat type
            if seat_type.venues.first().managers.contains(request.user):
                venue = seat_type.venues.first()
                # User has all permissions. Delete the seat type.
                seat_type.delete()
                return render(request, 'venue_management/manage_venue.html', {
                    'success_message': "Successfully deleted the seat type!",
                    'venue': venue,
                    'redirect': True
                })
            # The user isn't a manager of the venue that manages this seat type
            return render(request, 'venue_management/panel.html', {
                'error_message': "You are not a manager of the venue that controls this!",
                'venues': venues,
                'redirect': True
            })
        # The seat type doesn't exist
        return render(request, 'venue_management/panel.html', {
            'error_message': "This seat type does not exist!",
            'venues': venues,
            'redirect': True
        })
    # User not logged in
    return redirect('/venue/logout')


def set_restrictions(request, concert_id):
    """
    Sets the restrictions for the given concert
    :param request: (Django) object of the request's properties
    :param concert_id: the ID of the concert to
    :return:
    """
    if request.user.is_authenticated and not isinstance(request.user, VenueManager):
        return redirect('/venue/logout')
    if not request.user.is_authenticated:
        return redirect('/venue/login')

    # Ensure the user has permission to do this
    if request.method == 'POST' and isinstance(request.user, VenueManager):
        venues = request.user.venues.all()
        if len(venues) == 0:
            venues = None

        # Check if the concert exists
        if Concert.objects.filter(pk=concert_id).exists():
            concert = Concert.objects.get(pk=concert_id)

            # Check if the user is a manager of the venue containing the concert
            if concert.venues.first().managers.contains(request.user):
                venue = concert.venues.first()

                # Loop over all expected returns
                for seat_entry in venue.seat_types.all():
                    # Get the values from the POST and add to db
                    available = int(request.POST[f'{seat_entry.id}-available'])

                    # Try to update one if it exists already
                    try:
                        # If it exists, update the restriction.
                        restriction = concert.restrictions.get(seat_type=seat_entry)
                        restriction.available = available
                        restriction.save()
                    except SeatRestriction.DoesNotExist:
                        # Doesn't exist. Create a new seat restriction object
                        restriction = SeatRestriction(seat_type=seat_entry, concert=concert, available=available)
                        restriction.save()

                # Redirect the user
                return redirect(f"/venue/panel/concert/{concert_id}")

    return redirect('/venue/logout/')
