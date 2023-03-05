"""
views.py - Responsible for handling this application's views
"""

# Imports
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string

from .forms import RegisterForm, PromoCodeForm
from .models import VenueManager, PromoCode, Concert

def index(request):
    """
    The default index view for the Venue Management panel.
    :param request: (Django) object of the request's properties
    :return:
    """
    return render(request, 'venue_management/index.html')


def login_manager_window(request):
    """
    The login page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the login page
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email , password=password, model=VenueManager)

        if user is not None:
            login(request, user)
            return redirect('/')

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
    if request.method == "POST":
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password, model=VenueManager)

            print(user)
            login(request, user)
            return redirect('/venue/login')  # needs to specify where the redirect page goes
    else:
        form = RegisterForm()
    return render(request, 'venue_management/register.html', {'form': form})


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


def all_concerts(request):
    """All concerts models retrieves all the concerts from the database  and using paginator the data is passed to the
      html"""
    concert_list = Concert.objects.all()
    # arguments to call to your database, and how many arguments you want per page
    p = Paginator( Concert.objects.all(),3)
    page = request.GET.get('page')
    concerts = p.get_page(page)

    return render(request,'venue_management/concert.html',{'concerts':concert_list, 'conc':concerts})


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
