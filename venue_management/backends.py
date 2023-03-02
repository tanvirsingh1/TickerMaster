"""
Backend authenticating manager
"""

from django.contrib.auth.backends import BaseBackend
from .models import VenueManager

class VenueManagerBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            venuemanager = VenueManager.objects.get(email=email)
            if venuemanager.check_password(password):
                return venuemanager
        except VenueManager.DoesNotExist:
            pass
        return None
    def get_user(self, user_id):
        try:
            return VenueManager.objects.get(pk=user_id)
        except VenueManager.DoesNotExist:
            return None
