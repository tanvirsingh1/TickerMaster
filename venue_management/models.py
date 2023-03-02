"""
models.py - Contains all data models for the application
"""

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core import validators


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


class PromoCode(models.Model):
    """
    TODO: What's this?
    """
    code = models.CharField(max_length=20, unique=True, validators=[
                            validators.RegexValidator(r'^[a-zA-Z0-9]*$', 'Only letters and numbers are allowed.')])
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    expiration_date = models.DateField()
    venue_manager = models.ForeignKey(VenueManager, on_delete=models.CASCADE)
    generated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns the object's promo code
        :return: the promo code
        """
        return str(self.code)
