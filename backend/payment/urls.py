"""
URLs for Payment
"""

from django.urls import path
from .views import (
    CreatePayPalPaymentView,
    ExecutePayPalPaymentView,
    CancelPaymentView,
)

urlpatterns = [
    # create a payment and redirect the user to PayPal for approval
    path(
        "create-paypal-payment/",
        CreatePayPalPaymentView.as_view(),
        name="create-paypal-payment",
    ),
    # finalize the payment after approval from PayPal
    path(
        "execute-paypal-payment/",
        ExecutePayPalPaymentView.as_view(),
        name="execute-payment",
    ),
    path(
        "cancel-payment/", CancelPaymentView.as_view(), name="cancel-payment"
    ),
]
