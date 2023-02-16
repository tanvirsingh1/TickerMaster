from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegisterForm
from django.http import HttpResponse
# Create your views here.
def _login_window_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid username or password. Please try again.'
            print(error)
            return render(request, 'login/login.html', {'messages': error})

    return render(request, 'login/login.html');

def _register_window_(request):
    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registered Succesfully.')
            return redirect('#') # needs to specify where the redirect page goes
    else:
        form = RegisterForm()
    return render(request, 'login/register.html',{'form':form})