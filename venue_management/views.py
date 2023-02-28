"""
views.py - Responsible for handling this application's views
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from .models import VenueManager
from .backends import VenueManagerBackend
def login_Manager_window(request):
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
