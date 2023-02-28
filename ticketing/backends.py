from django.contrib.auth.backends import BaseBackend
from .models import Eventgoer

class EventgoerBackend(BaseBackend):
    """
    Custom authentication backend for Eventgoer model
    """

    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            eventgoer = Eventgoer.objects.get(email=email)
            if eventgoer.check_password(password):
                return eventgoer
        except Eventgoer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Eventgoer.objects.get(pk=user_id)
        except Eventgoer.DoesNotExist:
            return None