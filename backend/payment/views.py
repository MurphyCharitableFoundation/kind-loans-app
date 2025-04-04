"""Payment Views."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework.response import Response
from rest_framework.views import APIView

from loan.services import lender_make_payment, lender_receive_payment
from .models import Payment
from .services import (
    paypal_payment_create,
    paypal_payment_capture,
    paypal_payment_cancel,
    paypal_payout_create,
)


User = get_user_model()


class CreatePayPalPaymentView(APIView):
    """Create PayPal Payment View."""

    def post(self, request):
        """Create PayPal Payment."""
        amount = request.data.get("amount")
        currency = request.data.get("currency", "USD")
        payer_id = request.data.get("payer_id")
        return_url = request.build_absolute_uri(reverse("paypal-capture"))
        cancel_url = request.build_absolute_uri(reverse("cancel-payment"))

        if not amount:
            return Response({"amount": "Amount is required."}, status=400)

        payer = get_object_or_404(User, pk=payer_id)
        paypal_payment_data = paypal_payment_create(
            payer=payer,
            amount=amount,
            currency=currency,
            return_url=return_url,
            cancel_url=cancel_url,
        )

        return Response(paypal_payment_data, status=201)


class CapturePayPalPaymentView(APIView):
    """Execute PayPal Payment View."""

    def get(self, request):
        """Capture PayPal Payment."""
        try:
            payment_id = request.GET.get("token")
            paypal_payment_capture_data = paypal_payment_capture(
                payment_id=payment_id,
                capture_payment_func=lender_make_payment,
            )
            return Response(paypal_payment_capture_data)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CancelPayPalPaymentView(APIView):
    """Cancel PayPal Payment View."""

    def get(self, request):
        """Cencel PayPal Payment."""
        try:
            payment_id = request.GET.get("paymentId")
            paypal_payment_cancel(payment_id=payment_id)
            return Response(
                {"message": "Payment canceled."},
                status=200,
            )
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CapturePayPalPayoutView(APIView):
    """Capture PayPal Payout View."""

    def post(self, request):
        """Capture PayPal Payout."""
        # user = request.user
        payee_id = request.data.get("payee_id")
        amount = request.data.get("amount")

        if not amount:
            return Response({"amount": "Amount is required."}, status=400)

        payee = get_object_or_404(User, pk=payee_id)

        try:
            payout_data = paypal_payout_create(
                user=payee,
                amount=amount,
                capture_payout_func=lender_receive_payment,
                note=f"Withdrawal by {payee.email}",
            )

            return Response(payout_data, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
