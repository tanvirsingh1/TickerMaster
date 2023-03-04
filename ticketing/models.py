"""
models.py - Contains all data models for the application
"""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from .manager import UserManager
from django.contrib.auth.models import User


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
    UserName = None
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(max_length=40, unique=True, verbose_name='Email')
    is_active = models.BooleanField(verbose_name='Is Active', default=True)
    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_superuser = models.BooleanField(
        verbose_name='Is Superuser', default=False)
    is_reseller = models.BooleanField(verbose_name='Reseller Account')

    # Django attributes
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_reseller']
    objects = UserManager()

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

    def has_perm(self, *, _):
        """
        Checks if the Eventgoer is a superuser.
        TODO: Should check if they have the provided permission.
        :param _: (unused) the permission to check
        :return: whether the eventgoer is a superuser
        """
        return self.is_superuser

    def has_module_perms(self, _):
        """
        Checks if the admin has permissions for the given module
        TODO: Actually implement a permission check
        :param _: (unused) The label of the module to check against
        :return: Whether the user is a superuser
        """
        return self.is_superuser


class Concert(models.Model):
    """
    Class for Concert
    """
    artist_name = models.CharField(max_length=100)
    concert_date = models.DateTimeField()
    venue = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # Add any other fields that you need for your concert model


# class for support tickets
class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
