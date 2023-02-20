"""
views.py - Responsible for handling this application's views
"""

from django.http import HttpResponse
# from django.shortcuts import render


def index(_):
    """
    The default index view for the Venue Management panel.
    :param _: (throwaway) request parameter
    :return:
    """
    return HttpResponse("This is the Venue_Management index.")
