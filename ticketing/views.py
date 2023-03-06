"""
views.py - Responsible for handling this application's views
"""

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, SupportTicketForm
from .models import Eventgoer
from venue_management.models import Concert
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


#FOR CHECKOUT PAGE (SELECT AND BUY TICKETS)
def purchase_ticket(request):
    """
    select a ticket --> login, registration required
    """
    #check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')

    user = request.user
    #concert = request.concert

    #retrieve data from form
    if request.method == 'POST':

        quantity = int(request.POST.get('quantity'))
        print(quantity)
        if quantity == 0:
            error = "Please, select your ticket(s)."

            #promo_code = PromoCode.objects.get(code=request.POST.get('promo'))

            return render(request, 'ticketing/purchase_ticket.html', {'messages': error, 'user': user,
                                                                       'type' : 'select-tickets'})
            #return render(request, f'Ticketing_manager/purchase_ticket.html/{concert.id}', {'messages': error, \
            # 'user': user, 'concert': concert})
        return render(request, 'ticketing/purchase_ticket.html', {'user': user, 'type' : 'make-payment'})

    print("User is making a payment")
    # pass the current user object to the template context
    #return render(request, f'Ticketing_manager/purchase_ticket.html/{concert.id}', {'user': user, 'concert': concert})
    return render(request, 'ticketing/purchase_ticket.html', {'user': user, 'type' : 'select-tickets'})

def all_concerts(request):
    """All concerts models retrieves all the concerts from the database  and using paginator the data is passed to the
      html"""
    concert_list = Concert.objects.all()
    # arguments to call to your database, and how many arguments you want per page
    p = Paginator( Concert.objects.all(),3)
    page = request.GET.get('page')
    concerts = p.get_page(page)
    return render(request, 'Ticketing/concert.html', {'concerts':concert_list, 'conc':concerts})

def buy(request, concert_id):
    """Buy concept based on the selected concert"""
    # Retrieve the selected concert using the concert_id parameter
    concert = Concert.objects.get(pk=concert_id)
    # Pass the concert data to the template
    context = {'concert': concert}
    return render(request, 'Ticketing/buy.html', context)
