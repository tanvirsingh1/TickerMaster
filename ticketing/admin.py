"""
admin.py - Responsible for managing custom logic for the admin interface
"""

from django.contrib import admin
from . import models

# Register models with the admin site.
admin.site.register(models.Eventgoer)
admin.site.register(models.Order)
admin.site.register(models.Ticket)
admin.site.register(models.PaymentInfo)
