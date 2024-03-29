"""
models.py - Contains all data models for the application
"""

import math
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.core import validators

from .manager import UserManager


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
    is_active = models.BooleanField(verbose_name='Is Active', default=True)

    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_superuser = models.BooleanField(verbose_name='Is Superuser', default=False)

    # Django attributes
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

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

    def has_perm(self, *_):
        """
        Checks if the Venue Manager is a superuser.
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

    def __str__(self):
        """
        Gets the name and email of the venue manager
        :return: name and email of the venue manager
        """
        return f"{self.first_name} {self.last_name} ({self.email})"

    class DoesNotExist(Exception):
        """
        Bypasses the DoesNotExist exception for the venue manager account
        """


class Location(models.Model):
    """
    Describes a location/address
    """

    class Province(models.TextChoices):
        """
        A list of valid provinces
        """
        ALBERTA = 'AB', "Alberta"
        BRITISH_COLUMBIA = 'BC', "British Columbia"
        MANITOBA = 'MB', "Manitoba"
        NEW_BRUNSWICK = 'NB', "New Brunswick"
        NEWFOUNDLAND = 'NL', "Newfoundland and Labrador"
        NORTHWEST_TERRITORIES = 'NT', "Northwest Territories"
        NOVA_SCOTIA = 'NS', "Nova Scotia"
        NUNAVUT = 'NU', "Nunavut"
        ONTARIO = 'ON', "Ontario"
        PEI = 'PE', "Prince Edward Island"
        QUEBEC = 'QC', "Quebec"
        SASKATCHEWAN = 'SK', "Saskatchewan"
        YUKON_TERRITORIES = 'YT', "Yukon Territories"

    # --- Member Values ---
    street_num = models.IntegerField(validators=(
        validators.MinValueValidator(limit_value=1),
        validators.MaxValueValidator(limit_value=100_000)
    ))
    street_name = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    province = models.CharField(max_length=2, choices=Province.choices)

    def __str__(self):
        """
        :return: a string representation of the address
        """
        return f"{self.street_num} {self.street_name}, {self.city}, {self.get_province()}"

    def get_province(self):
        """
        Gets the name of the province that is associated with this location
        :return: name of the province
        """
        return self.Province(self.province)


class Concert(models.Model):
    """
    A class describing a concert
    """
    name = models.CharField(max_length=60, default='')
    artist_name = models.CharField(max_length=100)
    concert_date = models.DateTimeField()
    min_age = models.IntegerField(verbose_name="Minimum Age", null=True, validators=(
        validators.MinValueValidator(limit_value=1),
        validators.MaxValueValidator(limit_value=100)
    ))
    concert_image = models.ImageField(null=True, blank=True)
    description = models.TextField(blank=True)

    # venue - created by the ManyToMany field in Venue
    # restrictions - created by ForeignKey in SeatRestriction

    def __str__(self):
        """
        :return: the concert's name
        """
        return str(self.name)


class SeatType(models.Model):
    """
    Holds the name and quantity of a particular seat type.
    """
    name = models.CharField(max_length=60, verbose_name="Seat Type")
    quantity = models.IntegerField(verbose_name="Number of Seats", validators=(
        validators.MinValueValidator(limit_value=1),
        validators.MaxValueValidator(limit_value=1_000_000)
    ))
    price = models.FloatField(verbose_name="Price", validators=(
        validators.MinValueValidator(limit_value=0),
        validators.MaxValueValidator(limit_value=100_000)
    ))

    # venue - created by the ManyToMany field in Venue

    def __str__(self):
        """
        :return: the seat type's name
        """
        return str(self.name)


class SeatRestriction(models.Model):
    """
    Holds a seating restriction for a specific seat type on a Concert.
    """
    available = models.IntegerField(verbose_name="Percent Available", validators=(
        validators.MinValueValidator(limit_value=0),
        validators.MaxValueValidator(limit_value=100)
    ))
    seat_type = models.ForeignKey(SeatType, on_delete=models.deletion.CASCADE, verbose_name="Seat Type")
    concert = models.ForeignKey(Concert, on_delete=models.deletion.CASCADE, verbose_name="Concert",
                                related_name="restrictions")

    def get_available_seats(self):
        """
        Will calculate and return the number of available seats of this type
        for the associated Concert.
        :return: available seats of this type for the associated concert
        """
        return math.floor(self.seat_type.quantity * (self.available / 100))


class Venue(models.Model):
    """
    Describes a Venue
    """
    name = models.CharField(max_length=60, verbose_name="Name")
    description = models.CharField(max_length=255, verbose_name="Description", default=None)
    image = models.ImageField(max_length=255, verbose_name="Image")
    website = models.URLField(max_length=255, verbose_name="Website", null=False)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, verbose_name="Location")

    # ManyToManyField: https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
    seat_types = models.ManyToManyField(SeatType, verbose_name="Seat Types", related_name="venues")
    concerts = models.ManyToManyField(Concert, verbose_name="Concerts", related_name="venues")
    managers = models.ManyToManyField(VenueManager, verbose_name="Managers", related_name="venues")

    def __str__(self):
        """
        :return: the venue's name
        """
        return str(self.name)


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

    def get_discount(self):
        """
        Returns discount percent
        :return: discount
        """
        return self.discount
