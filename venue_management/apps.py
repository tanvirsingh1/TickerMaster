"""
apps.py - Responsible for storing the application's metadata
"""

from django.apps import AppConfig


class VenueManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'venue_management'
