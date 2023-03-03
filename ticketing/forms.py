"""
forms.py - Responsible for defining forms for the Ticketing application
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Eventgoer
from .models import Concert


class RegisterForm(UserCreationForm):
    """
    The registration form for Eventgoers. Creates an account when valid info is given.
    """
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your  Last Name'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))
    is_reseller = forms.BooleanField(label='Are you a Reseller?',
                widget=forms.RadioSelect(choices=[(True, 'Yes'),(False, 'No')]))

    class Meta:
        """
        Defines the form's metadata
        """
        model = Eventgoer
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email', 'is_reseller']



class ConcertForm(forms.ModelForm):
    """
    A form that allows for the registration of a concert. ???
    TODO: Figure out what this is and whether it should be here.
    """

    class Meta:
        """
        Metadata for the Concert Form
        """
        model = Concert
        fields = ['artist_name', 'concert_date', 'venue', 'city', 'country']
        # Add any other fields that you need for your concert form