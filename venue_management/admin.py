"""
admin.py - Responsible for managing custom logic for the admin interface
"""

from django.contrib import admin
from . import models

# Register models with the Admin site.
admin.site.register(models.VenueManager)