"""
urls.py - Responsible for defining URL routing for the Venue Management application
"""

from django.urls import path, include
from .views import generate_promo_code
from . import views

urlpatterns = [
    path('/ven', views.index, name='index'),
    path('generate-promo-code/', generate_promo_code, name='generate_promo_code')
]
