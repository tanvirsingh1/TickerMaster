"""
urls.py - Responsible for defining URL routing for the Ticketing application
"""

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_window, name="Login Window" ),
    path('register', views.register_window, name="Register Window"),
    path('concert-window-display/', views.concert_window, name="View Concerts"),
    path('support/', views.support_ticket, name="Support Ticket Form"),
    path('purchase-ticket/', views.purchase_ticket, name='Purchase Ticket')
    #path('purchase-ticket/<int:concert_id>/', views.purchase_ticket, name='purchase_ticket')
]