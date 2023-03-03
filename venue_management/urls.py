"""
urls.py - Responsible for defining URL routing for the Venue Management application
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_manager_window, name="Login Window" ),
    path('register/', views.register_manager_window, name="Register Window"),
    path('generate-promo-code/', views.generate_promo_code, name='generate_promo_code')
]
