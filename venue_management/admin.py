"""
admin.py - Responsible for managing custom logic for the admin interface
"""

from django.contrib import admin
from . import models


# Register models with the Admin site.
admin.site.register(models.VenueManager)
admin.site.register(models.Venue)
admin.site.register(models.Concert)
admin.site.register(models.Location)
admin.site.register(models.SeatType)
admin.site.register(models.SeatRestriction)
