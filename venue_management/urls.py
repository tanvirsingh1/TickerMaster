"""
urls.py - Responsible for defining URL routing for the Venue Management application
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_Manager_window, name="Login Window" ),
    path('register', views.register_Manager_window, name="Register Window")
]
