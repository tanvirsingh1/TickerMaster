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
    path('account/', views.account, name="account"),
    path('add_venue/', views.add_venue, name="add_venue"),
    path('edit_venue/<int:venue_id>/', views.edit_venue, name="edit_venue"),
    path('delete_venue/<int:venue_id>/', views.delete_venue, name="delete_venue"),
    path('delete_concert/<int:concert_id>/', views.delete_concert, name="delete_concert"),
    path('panel/', views.panel, name="panel"),
    path('panel/<int:venue_id>/', views.manage_venue, name='manage_venue'),
    path('panel/<int:venue_id>/add_seat', views.add_seat, name='add_seat'),
    path('panel/edit_seat/<int:seat_id>', views.edit_seat, name='edit_seat'),
    path('panel/delete_seat/<int:seat_id>', views.delete_seat, name='delete_seat'),
    path('panel/concert/<int:concert_id>/', views.manage_concert, name='manage_concert'),
    path('logout/', views.logout, name="logout"),
    path('generate-promo-code/', views.generate_promo_code, name='generate_promo_code'),
    path('add_concert/<int:venue_id>/', views.add_concert, name='add_concert'),
    path('edit_concert/<int:concert_id>/', views.edit_concert, name="edit_concert"),
    path('set_restrictions/<int:concert_id>/', views.set_restrictions, name="set_restrictions")
]
