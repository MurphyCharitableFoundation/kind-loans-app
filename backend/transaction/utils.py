from django.conf import settings

import paypalrestsdk
import string
import random


def generate_unique_code(length=8):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


def configure_paypal():
    paypalrestsdk.configure(
        {
            "mode": "sandbox",
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_SECRET_KEY,
        }
    )
