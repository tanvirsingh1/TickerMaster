"""
models.py - Contains all data models for the application
"""

from datetime import date
from django.db import models
from django.core import validators
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import get_user_model

from venue_management.models import Concert, SeatType
from .manager import UserManager

User = get_user_model()


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
    balance = models.FloatField(verbose_name="User Balance", default=5000)

    is_active = models.BooleanField(verbose_name='Is Active', default=True)
    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_superuser = models.BooleanField(verbose_name='Is Superuser', default=False)
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


class PaymentInfo(models.Model):
    """
    Contains payment information for a user.
    """
    user = models.ForeignKey(Eventgoer, on_delete=models.deletion.CASCADE, verbose_name="Eventgoer",
                             related_name="payment_info")

    # Card details
    card_number = models.CharField(max_length=16, verbose_name="Credit Card Number", null=False)
    cvv = models.CharField(max_length=4, verbose_name="CVV", null=False)
    exp_month = models.CharField(max_length=2, verbose_name="Exipration month", null=False)
    exp_year = models.CharField(max_length=4, verbose_name="Exipration year", null=False)
    holder_name = models.CharField(max_length=100, verbose_name="Card Holder Name", null=False)


class SupportTicket(models.Model):
    """
    Model representing a support ticket.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns the subject of the support ticket as a string.
        """
        return str(self.subject)

class Ticket(models.Model):
    """
    Describes a ticket that is purchased for a concert
    """
    seat_type = models.ForeignKey(SeatType, on_delete=models.deletion.CASCADE,
                                    verbose_name="Seat Type")
    concert = models.ForeignKey(Concert, on_delete=models.deletion.CASCADE, verbose_name="Concert",
                                    related_name="tickets")



class Order(models.Model):
    """
    Describes an Order for the purchase
    """

    purchaser = models.ForeignKey(Eventgoer, on_delete=models.deletion.CASCADE,
                                  verbose_name="Purchaser", related_name="orders")
    tickets = models.ManyToManyField(Ticket, verbose_name="Tickets", related_name="orders")
    payment_info = models.ForeignKey(PaymentInfo, verbose_name="Payment Info", on_delete=models.deletion.PROTECT, related_name="orders", null=True)

  #order info
    order_date = models.DateField(default=date.today)

    def order_total_price(self) -> float:
        """
        Gets the total price of all tickets in the order.
        :return: total price of all tickets in the order
        """
        price = 0
        for ticket in self.tickets.all():
            price += ticket.seat_type.price
        return price
