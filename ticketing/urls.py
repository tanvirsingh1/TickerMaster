"""
urls.py - Responsible for defining URL routing for the Ticketing application
"""

from django.urls import path
from . import views

app_name = 'ticketing'

urlpatterns = [
    path('', views.home_window, name='index'),
    path('about', views.about_window, name="about"),
    path('login', views.login_window, name="login"),
    path('register', views.register_window, name="register"),
    path('support/', views.support_ticket, name="support"),
    path('purchase-ticket/', views.purchase_ticket, name='purchase'),
    path('concerts/', views.all_concerts, name="list-concerts"),
    path('buy/<int:concert_id>/', views.buy, name='buy')
]
