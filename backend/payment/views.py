"""
Views for Payment
"""

from djmoney.money import Money
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from django.shortcuts import get_object_or_404

from core.models import User
from transaction.services import (
    create_paypal_transaction,
    execute_paypal_transaction,
    execute_paypal_payout_transaction,
)
from core.helpers import make_payment, make_payout


class CreatePayPalPaymentView(APIView):
    def post(self, request):
        amount_value = request.data.get("amount")
        currency = request.data.get("currency", "USD")
        payer_id = request.data.get("payer_id")
        return_url = request.build_absolute_uri(reverse("execute-payment"))
        cancel_url = request.build_absolute_uri(reverse("cancel-payment"))

        amount = Money(amount_value, currency)

        try:
            payer = get_object_or_404(User, pk=payer_id)

            payment, transaction = create_paypal_transaction(
                payer, amount, return_url, cancel_url
            )
            # Return the PayPal approval URL to the frontend
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return Response({"approval_url": approval_url}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=400)


class ExecutePayPalPaymentView(APIView):
    def get(self, request):
        payment_id = request.GET.get("paymentId")
        payer_id = request.GET.get("PayerID")

        try:
            execute_paypal_transaction(payment_id, payer_id, make_payment)

            return Response(
                {"message": "Payment completed successfully"}, status=200
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CancelPaymentView(APIView):
    def get(self, request):
        return Response({"message": "Payment was canceled."}, status=200)


class ExecutePayPalPayoutView(APIView):
    def post(self, request):
        payee_id = request.data.get("payee_id")
        amount_value = request.data.get("amount")
        currency = request.data.get("currency", "USD")

        amount = Money(amount_value, currency)

        try:
            # payee = request.user
            payee = get_object_or_404(User, pk=payee_id)

            execute_paypal_payout_transaction(payee, amount, make_payout)
            return Response({"message": "Payout executed."}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=400)
