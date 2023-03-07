"""
views.py - Responsible for handling this application's views
"""

from urllib.parse import urlencode
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.http import HttpResponseRedirect

from venue_management.models import Concert
from .forms import RegisterForm, SupportTicketForm
from .models import Eventgoer


def home_window(request):
    """
    The main index page
    :param request: (Django) object of the request's properties
    :return: ticketing/home.html
    """
    return render(request, 'ticketing/home.html')

def about_window(request):
    """
    The about us page
    :param request: (Django) object of the request's properties
    :return: ticketing/about.html
    """
    return render(request, 'ticketing/about.html')

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
            # needs to specify where the redirect page goes
            return redirect('/login')
    else:
        form = RegisterForm()
    return render(request, 'ticketing/register.html', {'form': form})


# support ticket view for storing customer complaints
def support_ticket(request):
    """
    support ticket Window
    """
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('support_ticket_success')
    else:
        form = SupportTicketForm()

    return render(request, 'ticketing/support_ticket.html', {'form': form})


# FOR CHECKOUT PAGE (SELECT AND BUY TICKETS)
def buy(request, concert_id):
    """
    select a ticket --> login, registration required
    """
    # check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')

    # get info about this request - info about user and concert
    user = request.user
    concert = Concert.objects.get(pk=concert_id)

    if request.method == 'POST':
        # retrieve data from form
        quantity = request.POST.get('quantity')

        #forming the customer's order
        order = []
        number_of_tickets = 0
        total = 0
        for i, quantity in enumerate(request.POST.getlist('quantity')):

            #order info
            quantity = int(quantity)
            number_of_tickets += quantity
            seat_name = concert.venues.first().seat_types.filter(id=(i+1)).first().name
            seat_price = concert.venues.first().seat_types.filter(id=(i+1)).first().price
            seats_available = concert.venues.first().seat_types.filter(id=(i+1)).first().quantity
            total += seat_price * quantity
            
            #in case user selected more tickets than available
            if seats_available < quantity:
                error = "Sorry, only " + str(seats_available) + " ticket(s) for Seat " + seat_name + " available."
                return render(request, 'ticketing/buy.html', {'messages': error,
                            'concert': concert, 'user': user})
            
            #adding booked seat (and number to order)
            else:
                booked_seats = {'name': seat_name, 'price': seat_price, 'quantity': quantity}
                order.append(booked_seats)

        #in case user didn't select any tickets
        if number_of_tickets == 0:
            error = "Please, select your ticket(s)."
            return render(request, 'ticketing/buy.html', {'messages': error,
                            'concert': concert, 'user': user})
        
        #in case everything is okay, the user is ready to pay
        url = reverse('ticketing:pay') + '?' + urlencode({'total': total})
        return HttpResponseRedirect(url)

    # pass the user select tickets
    return render(request, 'ticketing/buy.html/', {'user': user, 'concert': concert})

def pay(request):
    """
    paying for selected tickets --> user must be logged in
    """
    # check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')
    
    total = request.GET.get('total')
    

    if request.method == 'POST':
        # retrieve data from form
        card_number = int(request.POST.get('card_number'))
        cvv = request.POST.get('cvv')
        exp_month = request.POST.get('expiration_month')
        exp_year = request.POST.get('expiration_year')
        holder_name = request.POST.get('holder_name')

        #in case everything is okay, the user has successfully purchased tickets
        return render(request, 'ticketing/purchase-success.html')

    # pass the user make a payment
    return render(request, 'ticketing/payment.html/', {'total': total})


def all_concerts(request,concert=None,error=None):
    """All concerts models retrieves all the concerts from the database  and using paginator the data is passed to the
      html"""
    if concert:
        print(concert)
        concert2 = [concert]
        return render(request, 'Ticketing/concert.html', {'conc': concert2})

    concert_list = Concert.objects.all()
    # arguments to call to your database, and how many arguments you want per page
    p = Paginator( Concert.objects.all(),3)
    page = request.GET.get('page')
    concerts = p.get_page(page)
    return render(request, 'Ticketing/concert.html', {'concerts':concert_list, 'conc':concerts,'error':error})

def searched(request):
    """Search each concert based on the value, if value matches that concert shall be displayed, else nothing"""
    if request.method == "POST":
        print("Post request")
        search = request.POST["searched"]

        if not search:
            return redirect("/concerts")

        try:
            concert = Concert.objects.get(artist_name__iexact=search)
            return all_concerts(request, concert)
        except Concert.DoesNotExist:
            error = f"No Concerts by {search}"
            return all_concerts(request,None, error)

    else:
        return render(request, "/concerts")