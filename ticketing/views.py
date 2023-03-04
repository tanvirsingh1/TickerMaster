"""
views.py - Responsible for handling this application's views
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, SupportTicketForm
from .models import Eventgoer, Concert
from django.contrib.auth.decorators import login_required


def login_window(request):
    """
    The login page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the login page
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password, model=Eventgoer)

        if user is not None:
            login(request, user)
            return redirect('/')

        error = 'Invalid username or password. Please try again.'
        print(error)
        return render(request, 'ticketing/login.html', {'messages': error})

    return render(request, 'ticketing/login.html')


def register_window(request):
    """
    The registration page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the registration page
    """
    if request.method == "POST":

        form = RegisterForm(data=request.POST)
        print(form.errors)

        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password, model=Eventgoer)
            login(request, user)
            return redirect('/login')  # needs to specify where the redirect page goes
    else:
        form = RegisterForm()
    return render(request, 'ticketing/register.html', {'form': form})


def concert_window(request):
    """
    The concert window
    TODO: Find out what this does...
    :param request: (Django) object of the request's properties
    :return:
    """
    concerts = Concert.objects.all()
    context = {'concerts': concerts}
    return render(request, 'ticketing/concert_window.html', context)


#support ticket view for storing customer complaints
def support_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            support_ticket = form.save(commit=False)
            support_ticket.user = request.user
            support_ticket.save()
            return redirect('support_ticket_success')
    else:
        form = SupportTicketForm()

    return render(request, 'ticketing/support_ticket.html', {'form': form})