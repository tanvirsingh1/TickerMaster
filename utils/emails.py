"""
Email Sending Function
"""

# Imports
from typing import List
from smtplib import SMTPException
from django.core.mail import send_mail

def send_email(recipient: List[str], subject: str, message: str = None, html_message: str = None) -> None:
    """
    Sends an email using the email system (if email support is configured).
    :param recipient: the address to send the message to.
    :param subject: the subject line of the email.
    :param message: a plain-text version of the email.
    :param html_message: (OPTIONAL) an HTML version of the email to be displayed by supported clients.
    """

    try:
        # Check if the message provides an HTML version.
        if html_message is not None:
            # Send the email using Django's mail delivery (including HTML)
            send_mail(subject=subject, message=message, html_message=html_message,
                                recipient_list=[recipient], from_email=None)
        else:
            # Send the email using Django's mail delivery (plain text)
            send_mail(subject=subject, message=message,
                               recipient_list=[recipient], from_email=None)
    except SMTPException:
        print("WARN: Attempted to send an email, but email support from .env is either not configured or invalid.")
