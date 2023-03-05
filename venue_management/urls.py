"""
urls.py - Responsible for defining URL routing for the Venue Management application
"""

from django.urls import path
from . import views

app_name = 'venue_management'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_manager_window, name="login"),
    path('register/', views.register_manager_window, name="register"),
    path('concerts/',views.all_concerts, name = "list-concerts" ),
    path('panel/', views.panel, name="panel"),
    path('logout/', views.logout, name="logout"),
    path('generate-promo-code/', views.generate_promo_code, name='generate_promo_code'),
    path('add_concert/', views.add_concert, name='add_concert'),
    path('buy/<int:concert_id>/', views.buy, name='buy')
]
