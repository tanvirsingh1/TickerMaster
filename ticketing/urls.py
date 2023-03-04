"""
urls.py - Responsible for defining URL routing for the Ticketing application
"""

from django.urls import path
from . import views

app_name = 'ticketing'

urlpatterns = [
    path('login', views.login_window, name="login"),
    path('register', views.register_window, name="register")
]
