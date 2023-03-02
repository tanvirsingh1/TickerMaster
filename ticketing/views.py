from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from .models import Eventgoer


def login_window(request):

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

    if request.method == "POST":

        form = RegisterForm(data=request.POST)
        print(form.errors)

        if form.is_valid():

            form.save()

            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password, model=Eventgoer)
            print("user is " )
            print(user)
            login(request, user)
            return redirect('/login')  # needs to specify where the redirect page goes
    else:
        form = RegisterForm()
    return render(request, 'ticketing/register.html', {'form': form})