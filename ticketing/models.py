"""
models.py - Contains all data models for the application
"""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Eventgoer(AbstractBaseUser):
    """
    Sets out the attributes for an Event-goer's account
    """

    class Meta:
        """
        Metadata describing the Eventgoer model
        """
        verbose_name = "Eventgoer"
        verbose_name_plural = "Eventgoers"

    # Account Attributes
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(max_length=40, unique=True, verbose_name='Email')
    is_active = models.BooleanField(verbose_name='Is Active')
    is_reseller = models.BooleanField(verbose_name='Reseller Account')

    # Django attributes
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'is_reseller']

    def __str__(self):
        return f"{self.get_full_name()} (Reseller)" if self.is_reseller else self.get_full_name()

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


class Concert(models.Model):
    """
    Concert Window displaying Concerts???
    TODO: Figure out what this is and whether it should be here.
    """
    artist_name = models.CharField(max_length=100)
    concert_date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # Add any other fields that you need for your concert model
