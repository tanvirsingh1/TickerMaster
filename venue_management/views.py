"""
views.py - Responsible for handling this application's views
"""

from django.http import HttpResponse
# from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import PromoCodeForm
from .models import PromoCode
from django.utils.crypto import get_random_string
from django.contrib import messages
from random import randint

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings


def index(_):
    """
    The default index view for the Venue Management panel.
    :param _: (throwaway) request parameter
    :return:
    """
    return HttpResponse("This is the Venue_Management index.")


# @login_required
# @require_http_methods(["GET", "POST"])
def generate_promo_code(request):
    if request.method == "POST":
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            # Generate Promo Code
            promo_code = PromoCode.objects.create(
                code=form.cleaned_data["discount"],
                discount=form.cleaned_data["discount"],
                expiration_date=form.cleaned_data["expiration_date"],
            )

            # Render promo code on the screen
            context = {
                "promo_code": promo_code.code,
            }
            promo_code_html = render_to_string(
                "venue_management/promo_code.html", context
            )
            return HttpResponse(promo_code_html)
    else:
        form = PromoCodeForm()
    return render(request, "venue_management/generate_promo_code.html", {"form": form})