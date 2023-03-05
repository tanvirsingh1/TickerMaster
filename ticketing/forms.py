"""
forms.py - Responsible for defining forms for the Ticketing application
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Eventgoer, SupportTicket


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
    is_reseller = forms.TypedChoiceField(coerce=lambda x: x == 'True',
                                   choices=((False, 'No'), (True, 'Yes')))

    class Meta:
        """
        Defines the form's metadata
        """
        model = Eventgoer
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email', 'is_reseller']


class SupportTicketForm(forms.ModelForm):
    """
    A form for submitting a support ticket with a subject and message.
    """
    class Meta:
        """
        Form metadata for the SupportTicketForm.
        """
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
