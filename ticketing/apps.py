"""
apps.py - Responsible for storing the application's metadata
"""
from django.apps import AppConfig


class TicketSprintConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ticketing'
    verbose_name = 'Ticketing'
