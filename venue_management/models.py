"""
models.py - Contains all data models for the application
"""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class VenueManager(AbstractBaseUser):
    """
    Sets out the attributes for a Venue Manager's account.
    """

    class Meta:
        """
        Metadata describing the VenueManager model
        """
        verbose_name = "Venue Manager"
        verbose_name_plural = "Venue Managers"

    # Account Attributes
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(max_length=40, unique=True, verbose_name='Email')
    is_active = models.BooleanField(verbose_name='Is Active')

    # Django attributes
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    # Methods
    def get_full_name(self) -> str:
        """
        Gets the full name of the Venue Manager
        :return: full name of the Venue manager
        """
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self) -> str:
        """
        Gets the short, informal name of the Venue Manager
        :return: first name of the Venue Manager
        """
        return self.first_name
