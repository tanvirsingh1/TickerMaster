"""
forms.py - Responsible for defining forms for the Venue Management application
"""

# Imports
from django import forms


class PromoCodeForm(forms.Form):
    """
    TODO: What is this?
    """
    name = forms.CharField(label='Your Name')
