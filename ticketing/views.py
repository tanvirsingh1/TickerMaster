"""
views.py - Responsible for handling this application's views
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, SupportTicketForm
from .models import Eventgoer, Concert


def login_window(request):
    """
    The login page for the ticketing application. Accepts a username and password.
    :param request: (Django) object of the request's properties
    :return: the login page
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email,
                            password=password, model=Eventgoer)

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
            user = authenticate(request, email=email,
                                password=password, model=Eventgoer)
            login(request, user)
            # needs to specify where the redirect page goes
            return redirect('/login')
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

def purchase_ticket(request):

    """
    buying a ticket --> login, registration required
    """

    #check if the user is logged in
    if not request.user.is_authenticated:
        return redirect('/login')


    #retrieve data from form
    if request.method == 'POST':
        promo_code = request.POST.get('promo_code')
        quantity = int(request.POST.get('quantity'))

        if quantity == 0:
            error = "Please, select your tickets."
            return render(request, 'Ticketing_manager/purchase_ticket.html', {'messages': error, 'user': request.user})

    # pass the current user object to the template context
    return render(request, 'Ticketing_manager/purchase_ticket.html', {'user': request.user})

    if request.method == 'POST':
        #retrieve data from form
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        seating_type = request.POST.get('seating_type')
        price = request.POST.get('price')
        seats_available = request.POST.get('seats_available')
        
        
        #validation
        if not all([firstname, lastname, email, seating_type, price, seats_available]):
            # error message if any of the required fields are missing
            return render(request, 'purchase_ticket.html', {'error_message': 'Please fill in all required fields.'})
        
        #check if the promo code is valid
        if promo_code == 'SPECIAL50':
            price = int(price) * 0.5
        
        #calculate the total price
        total_price = price * quantity
        
        #store the data in session
        request.session['purchase_data'] = {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'seating_type': seating_type,
            'price': price,
            'seats_available': seats_available,
            'promo_code': promo_code,
            'quantity': quantity,
            'total_price': total_price,
        }
        
        #redirect to the next page
        return redirect('payment_info')
        
    else:
        return render(request, 'Ticketing_manager/purchase_ticket.html', {'form': form})