from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm your password'}))

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
