"""
views.py - Responsible for handling this application's views
"""

# Imports
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.template.loader import render_to_string

from .forms import RegisterForm, PromoCodeForm
from .models import VenueManager, PromoCode

def index(_):
    """
    The default index view for the Venue Management panel.
    :param _: (throwaway) request parameter
    :return:
    """
    return HttpResponse("This is the Venue_Management index.")

def login_manager_window(request):
    """
    The login page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the login page
    """
    if request.method == 'POST':
        email  = request.POST['email']

        password = request.POST['password']

        user = authenticate(request, email=email , password=password, model=VenueManager)

        if user is not None:
            login(request, user)
            return redirect('/')

        error = 'Invalid username or password. Please try again.'
        print(error)
        return render(request, 'Ticketing_manager/login.html', {'messages': error})

    return render(request, 'Ticketing_manager/login.html')


def register_Manager_window(request):
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
    return render(request, 'Ticketing_manager/register.html', {'form': form})


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
