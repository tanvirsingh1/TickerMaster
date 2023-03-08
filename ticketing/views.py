"""
views.py - Responsible for handling this application's views
"""

from urllib.parse import urlencode
import ast
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lo
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect

from venue_management.models import Concert, SeatType, Venue
from .forms import RegisterForm, SupportTicketForm, NotificationForm, CompareTicketsForm
from .models import Eventgoer, Ticket, Order


def home_window(request):
    """
    The main index page
    :param request: (Django) object of the request's properties
    :return: ticketing/home.html
    """
    concerts = Concert.objects.all()
    seat_type = SeatType.objects.all()
    venue = Venue.objects.all()

    return render(request, 'ticketing/home.html', {'concerts': concerts, 'seatype': seat_type, 'venue' : venue})


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


@login_required(login_url='/venue/login')
def logout(request):
    """
    Logs the current user out
    :param request: (Django) object of the request's properties
    :return: redirects home
    """
    lo(request)
    return redirect('/venue')

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

    # get info about this request - info about user and concert
    user = request.user
    concert = Concert.objects.get(pk=concert_id)

    # check if the user is logged in and is an Eventgoer
    if not user.is_authenticated:
        return redirect('/login')

    if not isinstance(user, Eventgoer):

        error = "Your account is registered as a Venue Manager. Only EventGoer accounts \
            can buy Tickets."
        return render(request, 'ticketing/home.html', {'concerts': Concert.objects.all(), \
                'seatype': SeatType.objects.all(), 'venue' : Venue.objects.all(), \
                'message': error, 'url': '/'})

    if request.method == 'POST':
        # retrieve data from form
        quantity = request.POST.get('quantity')

        #forming the customer's order
        booked_seats = []
        number_of_tickets = 0
        total = 0
        for i, quantity in enumerate(request.POST.getlist('quantity')):

            #order info
            quantity = int(quantity)
            number_of_tickets += quantity
            seat_name = concert.venues.first().seat_types.filter(id=i+1).first().name
            seat_price = concert.venues.first().seat_types.filter(id=i+1).first().price
            seats_available = concert.venues.first().seat_types.filter(id=i+1).first().quantity
            total += seat_price * quantity

            #in case user selected more tickets than available
            if seats_available - quantity < 0:
                error = "Sorry, only " + str(seats_available) + " ticket(s) for Seat " \
                    + seat_name + " available."
                return render(request, 'ticketing/buy.html', {'messages': error,
                            'concert': concert, 'user': user})

            #adding booked seat (and number to order)
            seat = {"id": i+1, "name": seat_name, "price": seat_price, "quantity": quantity}
            booked_seats.append(seat)

        #in case user didn't select any tickets
        if number_of_tickets == 0:
            error = "Please, select your ticket(s)."
            return render(request, 'ticketing/buy.html', {'messages': error,
                            'concert': concert, 'user': user})

        #in case everything is okay, the user is ready to pay
        url = reverse('ticketing:pay') + '?' + urlencode({'total': total, \
                    'booked_seats': booked_seats, 'concert_id': concert_id})
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


    if request.method == 'POST':

        #extracting past data
        total = request.POST.get('total')
        booked_seats = request.POST.get('booked_seats')
        concert_id = request.POST.get('concert_id')
        concert = Concert.objects.get(pk=concert_id)

        # retrieve data from form for a check
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')

        #in case user selected more tickets than available
        if not card_number.isdigit() or not cvv.isdigit():
            error = "The provided information is invalid."
            return render(request, 'ticketing/payment.html', {'messages': error, 'total': total, \
                                    'booked_seats': booked_seats, 'concert_id': concert_id})

        #in case everything is okay, the user has successfully purchased tickets
        # Create and save the new order
        order = Order(purchaser = request.user, card_number = card_number, cvv = cvv, \
        exp_month = request.POST.get('expiration_month'), \
            exp_year = request.POST.get('expiration_year'), \
            holder_name = request.POST.get('holder_name'), total = total)
        order.save()

        #update ticket's number in the database
        booked_seats = ast.literal_eval(booked_seats)
        for database_seats in concert.venues.first().seat_types.all():
            for ordered_seats in booked_seats:
                if database_seats.id == ordered_seats['id']:
                    database_seats.quantity -= ordered_seats['quantity']
                    database_seats.save()

        #create ticket in the database for each purchased ticket
        for ordered_seats in booked_seats:
            seattype = SeatType.objects.get(pk=ordered_seats['id'])
            for _ in range(ordered_seats['quantity']):
                ticket = Ticket(seat_type=seattype, concert=concert)
                ticket.save()
                order.tickets.add(ticket)

        #plainTextMessageVar = "Thank you for your purchase. Here are your tickets. Enjoy"
        #htmlMessageTextVar = ""
        #emails.send_email(recipient=user.email, subject="Your Tickets", \
        # message=plainTextMessageVar, html_message=htmlMessageTextVar)

        return render(request, 'ticketing/purchase-success.html')

    # pass the user make a payment
    total = request.GET.get('total')
    booked_seats = request.GET.get('booked_seats')
    concert_id = request.GET.get('concert_id')
    return render(request, 'ticketing/payment.html/', {'total': total, \
            'booked_seats': booked_seats, 'concert_id': concert_id})


#See orders for eventgoers
def view_orders(request):

    # get user of the request
    user = request.user

    # check if the user is logged in and is an Eventgoer
    if not user.is_authenticated:
        return redirect('/login')

    if not isinstance(user, Eventgoer):

        error = "Your account is registered as a Venue Manager. Only EventGoer accounts \
            can have orders."
        return render(request, 'ticketing/home.html', {'concerts': Concert.objects.all(), \
                'seatype': SeatType.objects.all(), 'venue' : Venue.objects.all(), \
                'message': error, 'url': '/'})
    
    print()
    # pass the user select tickets
    #return render(request, 'ticketing/order.html/', {'user': user, 'orders': user.orders.all})


def all_concerts(request, concert=None, error=None):
    """All concerts models retrieves all the concerts from the database  and using paginator the data is passed to the
      html"""
    if concert:
        print(concert)
        concert2 = [concert]
        return render(request, 'ticketing/concert.html', {'conc': concert2})

    concert_list = Concert.objects.all()
    # arguments to call to your database, and how many arguments you want per page
    p = Paginator(Concert.objects.all(), 3)
    page = request.GET.get('page')
    concerts = p.get_page(page)
    return render(request, 'ticketing/concert.html', {'concerts':concert_list, \
                                        'conc':concerts,'error':error})


def searched(request):
    """Search each concert based on the value, if value matches that concert
    shall be displayed, else nothing"""
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
            return all_concerts(request, None, error)

    else:
        return render(request, "/concerts")

def compare_tickets_view(request):
    """ compare tikcet view """
    form = CompareTicketsForm(request.POST or None)

    if form.is_valid():
        ticket_1 = form.cleaned_data['ticket_1']
        ticket_2 = form.cleaned_data['ticket_2']
        context = {
            'ticket_1': ticket_1,
            'ticket_2': ticket_2,
        }
    else:
        context = {
            'form': form,
        }

    return render(request, 'ticketing/compare_tickets.html', context)

def notifications(request):
    """ view for user notification """
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            notify_new = form.cleaned_data['notify_new']
            notify_cancelled = form.cleaned_data['notify_cancelled']

            # send email notifications based on form data
            subject = 'Event Notification Settings'
            message = f'You will receive notifications for new events: {notify_new}\n'
            message += f'You will receive notifications for cancelled events: {notify_cancelled}'
            from_email = 'noreply@example.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            # display confirmation message
            context = {'message': 'Notification settings saved!'}
            return render(request, 'ticketing/notifications.html', context)
    else:
        form = NotificationForm()

    context = {'form': form}
    return render(request, 'ticketing/notifications.html', context)
