"""Payment URLs."""

from django.urls import path

from .views import (
    CreatePayPalPaymentView,
    CapturePayPalPaymentView,
    CancelPayPalPaymentView,
    CapturePayPalPayoutView,
)

urlpatterns = [
    # create a payment and redirect the user to PayPal for approval
    path(
        "paypal/create/",
        CreatePayPalPaymentView.as_view(),
        name="paypal-create",
    ),
    # finalize the payment after approval from PayPal
    path(
        "paypal/capture/",
        CapturePayPalPaymentView.as_view(),
        name="paypal-capture",
    ),
    path(
        "paypal/cancel/",
        CancelPayPalPaymentView.as_view(),
        name="cancel-payment",
    ),
    path(
        "paypal/payout/",
        CapturePayPalPayoutView.as_view(),
        name="paypal-payout",
    ),
]
