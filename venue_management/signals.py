"""
signals.py - Handles events triggered in the venue_management application
"""

# Imports
from django.dispatch import receiver
from django.db.models.signals import pre_delete

from . import models

@receiver(pre_delete, sender=models.Venue)
def pre_delete_venue(_sender: models.Venue, instance: models.Venue, **_kwargs):
    """
    Called just before a venue is deleted. Will delete all seat types.
    :param _sender: the class of the model that triggered the signal
    :param instance: the instance of the model that triggered the signal
    :param _kwargs: * additional arguments *
    """
    # Iterate over all seat types and delete them
    for seat_type in instance.seat_types.all():
        seat_type.delete()

    # Iterate over all concerts and delete them
    for concert in instance.concerts.all():
        concert.delete()
