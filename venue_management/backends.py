from django.contrib.auth.backends import BaseBackend
from .models import VenueManager

class VenueManagerBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            eventgoer = VenueManager.objects.get(email=email)
            if eventgoer.check_password(password):
                return eventgoer
        except VenueManager.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return VenueManager.objects.get(pk=user_id)
        except VenueManager.DoesNotExist:
            return None