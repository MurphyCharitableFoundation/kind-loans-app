"""
Views for Payment
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from django.urls import reverse
from django.shortcuts import get_object_or_404

from core.models import User, LoanProfile
from payment.services import create_paypal_transaction, execute_paypal_transaction


class CreatePayPalPaymentView(APIView):
    def post(self, request):
        amount = request.data.get("amount")
        payer_id = request.data.get("payer_id")
        recipient_id = request.data.get("recipient_id")
        return_url = request.build_absolute_uri(reverse("execute-payment"))
        cancel_url = request.build_absolute_uri(reverse("cancel-payment"))

        try:
            payer = get_object_or_404(User, pk=payer_id)
            recipient = get_object_or_404(LoanProfile, pk=recipient_id)
            payment, transaction = create_paypal_transaction(
                payer, recipient, amount, return_url, cancel_url
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
            execute_paypal_transaction(payment_id, payer_id)    # -> payment

            return Response(
                {"message": "Payment completed successfully"}, status=200
            )
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class CancelPaymentView(APIView):
    def get(self, request):
        return Response({"message": "Payment was canceled."}, status=200)
