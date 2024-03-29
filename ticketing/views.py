"""
views.py - Responsible for handling this application's views
"""

from datetime import date
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as lo
from django.contrib.auth.decorators import login_required
from utils import emails

from venue_management.models import Concert, SeatType, Venue
from .forms import RegisterForm, SupportTicketForm, NotificationForm, CompareTicketsForm
from .models import Eventgoer, Ticket, Order, PaymentInfo


def home_window(request):
    """
    The main index page
    :param request: (Django) object of the request's properties
    :return: ticketing/home.html
    """
    concerts = Concert.objects.all()
    seat_type = SeatType.objects.all()
    venue = Venue.objects.all()

    return render(request, 'ticketing/home.html', {'concerts': concerts, 'seatype': seat_type, 'venue': venue})


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
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, 'ticketing/register.html', {'form': form})


@login_required(login_url='/login')
def logout(request):
    """
    Logs the current user out
    :param request: (Django) object of the request's properties
    :return: redirects home
    """
    lo(request)
    return redirect('/')


@login_required(login_url='/login')
def account(request):
    """
    Serves the Eventgoer's account details page and accepts updated form data.
    :param request: (Django) object of the request's properties
    :return: account details page
    """
    # Ensure the user is an eventgoer
    if isinstance(request.user, Eventgoer):
        # Check for a form submission
        if request.method == 'POST':
            # Process update form submission
            try:
                # Grab passwords from the form
                current_password = request.POST['password']
                if authenticate(request, email=request.user.email, password=current_password, \
                                model=Eventgoer):
                    request.user.first_name = request.POST['first_name']
                    request.user.last_name = request.POST['last_name']
                    if 'new_password' in request.POST.keys() and \
                            request.POST['new_password'] is not None \
                            and request.POST['new_password'] != "":
                        # Set the new password, if provided in the form
                        request.user.set_password(request.POST['new_password'])

                    # Save the user's account
                    request.user.save()
                    # User account information updated
                    return render(request, 'ticketing/account.html', {
                        "success_message": "Successfully updated account data!"
                    })
                # Provided password was incorrect
                return render(request, 'ticketing/account.html', {
                    "error_message": "The password you gave was incorrect. Please try again."
                })
            except (NameError, KeyError):
                # Invalid information received
                return render(request, 'ticketing/account.html', {
                    "error_message": "Failed to update account data! Invalid form contents received."
                })
        # Serve account page
        return render(request, 'ticketing/account.html')
    return redirect('venue_management:account')


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
        error = "Your account is registered as a Venue Manager. Only Eventgoer accounts can buy Tickets."
        return render(request, 'ticketing/home.html', {'concerts': Concert.objects.all(),
                                                       'seatype': SeatType.objects.all(), 'venue': Venue.objects.all(),
                                                       'message': error, 'url': '/'})

    if request.method == 'POST':
        # retrieve data from form
        quantity = request.POST.get('quantity')

        # forming the customer's order
        booked_seats = []
        number_of_tickets = 0
        total = 0
        for i, quantity in enumerate(request.POST.getlist('quantity')):

            # order info
            quantity = int(quantity)
            number_of_tickets += quantity
            seat_name = concert.venues.first().seat_types.filter(id=i + 1).first().name
            seat_price = concert.venues.first().seat_types.filter(id=i + 1).first().price
            seats_available = concert.venues.first().seat_types.filter(id=i + 1).first().quantity
            total += seat_price * quantity

            # in case user selected more tickets than available
            if seats_available - quantity < 0:
                error = "Sorry, only " + str(seats_available) + " ticket(s) for Seat " \
                        + seat_name + " available."
                return render(request, 'ticketing/buy.html', {'messages': error,
                                                              'concert': concert, 'user': user})

            # adding booked seat (and number to order)
            seat = {"id": i + 1, "name": seat_name, "price": seat_price, "quantity": quantity}
            booked_seats.append(seat)

        # in case user didn't select any tickets
        if number_of_tickets == 0:
            error = "Please, select your ticket(s)."
            return render(request, 'ticketing/buy.html', {'messages': error,
                                                          'concert': concert, 'user': user})

        # in case everything is okay, the user is ready to pay
        if request.user.balance - total >= 0:
            # in case everything is okay, the user has successfully purchased tickets
            # update database
            request.user.balance -= total
            request.user.save()

            for database_seats in concert.venues.first().seat_types.all():
                for ordered_seats in booked_seats:
                    if database_seats.id == ordered_seats['id']:
                        database_seats.quantity -= ordered_seats['quantity']
                        database_seats.save()

            # Create and save the new order
            order = Order(purchaser=request.user, order_date=date.today())
            order.save()

            # create ticket in the database for each purchased ticket
            for ordered_seats in booked_seats:
                seattype = SeatType.objects.get(pk=ordered_seats['id'])
                for _ in range(ordered_seats['quantity']):
                    ticket = Ticket(seat_type=seattype, concert=concert)
                    ticket.save()
                    order.tickets.add(ticket)

            confirmation = 'You have successfully purchased tickets on TicketSprint. \
                You can view your review your tickets in "My Orders" tab on TicketSprint website.'
            emails.send_email(recipient=request.user.email, subject="Purchase confirmation", \
                              message=confirmation)
        else:
            error = "You don't have enough balance to proceed. Please, add balance in \
                'Add Balance' tab."
            return render(request, 'ticketing/buy.html', {'messages': error,
                                                          'concert': concert, 'user': user})

        return render(request, 'ticketing/purchase-success.html')

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
        # retrieve data from form for a check
        card_number = request.POST.get('card_number')
        cvv = request.POST.get('cvv')
        total = request.POST.get('total')

        # in case user selected more tickets than available
        if not card_number.isdigit() or not cvv.isdigit():
            error = "The provided information is invalid."
            return render(request, 'ticketing/payment.html', {'messages': error})

        # in case everything is okay, the user has successfully purchased tickets
        # Create and save the payment info
        payment_info = PaymentInfo(user=request.user, card_number=card_number, cvv=cvv,
                                   exp_month=request.POST.get('expiration_month'),
                                   exp_year=request.POST.get('expiration_year'),
                                   holder_name=request.POST.get('holder_name'))
        payment_info.save()

        request.user.balance += int(total)
        request.user.save()

        return redirect('/')

    # pass the user make a payment
    return render(request, 'ticketing/payment.html/')


# See orders for eventgoers
def view_orders(request):
    """See all orders of the eventgoer"""

    # get user of the request
    user = request.user

    # check if the user is logged in and is an Eventgoer
    if not user.is_authenticated:
        return redirect('/login')

    if not isinstance(user, Eventgoer):
        error = "Your account is registered as a Venue Manager. Only Eventgoer accounts \
            can have orders."
        return render(request, 'ticketing/home.html', {'concerts': Concert.objects.all(),
                                                       'seatype': SeatType.objects.all(), 'venue': Venue.objects.all(),
                                                       'message': error, 'url': '/'})

    # pass the user select tickets
    return render(request, 'ticketing/order.html/', {'orders': request.user.orders.all()})


def all_concerts(request, concert=None, error=None):
    """All concerts models retrieves all the concerts from the database  and using paginator \
        the data is passed to the html"""
    if concert:
        print(concert)
        concert2 = [concert]
        return render(request, 'ticketing/concert.html', {'conc': concert2})

    concert_list = Concert.objects.all()
    # arguments to call to your database, and how many arguments you want per page
    p = Paginator(Concert.objects.all(), 3)
    page = request.GET.get('page')
    concerts = p.get_page(page)
    return render(request, 'ticketing/concert.html', {'concerts': concert_list, \
                                                      'conc': concerts, 'error': error})


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
