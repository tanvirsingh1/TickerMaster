"""
urls.py - Responsible for defining URL routing for the Ticketing application
"""

from django.urls import path
from . import views 

urlpatterns = [
    path('login', views.login_window, name="Login Window" ),
    path('', views.home_window, name="Home" ),
    path('register', views.register_window, name="Register Window"),
    path('concert-window-display/', views.concert_window, name="View Concerts")
]
