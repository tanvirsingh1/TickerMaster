"""
urls.py - Responsible for defining URL routing for the Venue Management application
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index')
]
