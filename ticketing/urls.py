"""
urls.py - Responsible for defining URL routing for the Ticketing application
"""

from django.urls import path
from . import views

app_name = 'ticketing'

urlpatterns = [
    path('login', views.login_window, name="login"),
    path('register', views.register_window, name="register"),
    path('concert-window-display/', views.concert_window, name="concerts"),
    path('support/', views.support_ticket, name="support"),
    path('purchase-ticket/', views.purchase_ticket, name='purchase')
    #path('purchase-ticket/<int:concert_id>/', views.purchase_ticket, name='purchase_ticket')
]
