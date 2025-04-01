"""Payment URLs."""

from django.urls import path

from .views import (
    CreatePayPalPaymentView,
    CapturePayPalPaymentView,
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
        "paypal/capture/<str:payment_id>/",
        CapturePayPalPaymentView.as_view(),
        name="paypal-capture",
    ),
    path(
        "paypal/payout/",
        CapturePayPalPayoutView.as_view(),
        name="paypal-payout",
    ),
]
