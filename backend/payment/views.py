"""Payment Views."""

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_serializer,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)


from loan.services import lender_make_payment, lender_receive_payment
from .models import Payment
from .services import (
    paypal_payment_create,
    paypal_payment_capture,
    paypal_payment_cancel,
    paypal_payout_create,
)


User = get_user_model()


@extend_schema_serializer(component_name="CreatePayPalPayment")
class CreatePayPalPaymentView(APIView):
    """Create PayPal Payment View."""

    class InputSerializer(serializers.Serializer):
        """PayPal Payment Input Serializer."""

        amount = serializers.CharField()
        currency = serializers.CharField(default="USD", required=False)
        payer_id = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        """PayPal Payment Output Serializer."""

        id = serializers.CharField()
        status = serializers.CharField(required=False)
        links = serializers.ListField(
            child=serializers.DictField(), required=False
        )

    @extend_schema(
        request=InputSerializer,
        responses={
            201: OutputSerializer,
            400: OpenApiResponse(description="Invalid or missing input."),
        },
        examples=[
            OpenApiExample(
                name="Valid Request",
                value={"amount": "10.00", "currency": "USD", "payer_id": 1},
                request_only=True,
            ),
            OpenApiExample(
                name="Valid Response",
                value={
                    "id": "7DL65867YS292100Y",
                    "status": "PAYER_ACTION_REQUIRED",
                    "payment_source": {"paypal": {}},
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/7DL65867YS292100Y",  # noqa
                            "rel": "self",
                            "method": "GET",
                        },
                        {
                            "href": "https://www.sandbox.paypal.com/checkoutnow?token=7DL65867YS292100Y",  # noqa
                            "rel": "payer-action",
                            "method": "GET",
                        },
                    ],
                },
                response_only=True,
            ),
        ],
    )
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


@extend_schema_serializer(component_name="CapturePayPalPayment")
class CapturePayPalPaymentView(APIView):
    """Execute PayPal Payment View."""

    class CapturePayPalInputSerializer(serializers.Serializer):
        """Input for capturing PayPal payment."""

        token = serializers.CharField(
            help_text="PayPal PaymentID or Token returned after user approval."
        )

    class CapturePayPalOutputSerializer(serializers.Serializer):
        """Output for captured PayPal payment response."""

        id = serializers.CharField()
        status = serializers.CharField()
        amount = serializers.DictField(required=False)
        links = serializers.ListField(
            child=serializers.DictField(), required=False
        )

    @extend_schema(
        request=CapturePayPalInputSerializer,
        parameters=[
            OpenApiParameter(
                name="token",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="PayPal order ID used to capture the payment.",
            )
        ],
        responses={
            200: CapturePayPalOutputSerializer,
            400: OpenApiResponse(description="Capture failed or bad request."),
            404: OpenApiResponse(description="Payment not found."),
        },
        examples=[
            OpenApiExample(
                name="Successful Capture",
                value={
                    "id": "6DL65867YS292100Y",
                    "status": "COMPLETED",
                    "payment_source": {
                        "paypal": {
                            "email_address": "lender@mcf.com",
                            "account_id": "TAE6M66KTEVRW",
                            "account_status": "VERIFIED",
                            "name": {"given_name": "John", "surname": "Doe"},
                            "address": {"country_code": "US"},
                        }
                    },
                    "purchase_units": [
                        {
                            "reference_id": "default",
                            "shipping": {
                                "name": {"full_name": "John Doe"},
                                "address": {
                                    "address_line_1": "1 Main St",
                                    "admin_area_2": "San Jose",
                                    "admin_area_1": "CA",
                                    "postal_code": "95131",
                                    "country_code": "US",
                                },
                            },
                            "payments": {
                                "captures": [
                                    {
                                        "id": "2D909796HK759514R",
                                        "status": "COMPLETED",
                                        "amount": {
                                            "currency_code": "USD",
                                            "value": "200.00",
                                        },
                                        "final_capture": True,
                                        "seller_protection": {
                                            "status": "ELIGIBLE",
                                            "dispute_categories": [
                                                "ITEM_NOT_RECEIVED",
                                                "UNAUTHORIZED_TRANSACTION",
                                            ],
                                        },
                                        "seller_receivable_breakdown": {
                                            "gross_amount": {
                                                "currency_code": "USD",
                                                "value": "200.00",
                                            },
                                            "paypal_fee": {
                                                "currency_code": "USD",
                                                "value": "6.10",
                                            },
                                            "net_amount": {
                                                "currency_code": "USD",
                                                "value": "193.90",
                                            },
                                            "receivable_amount": {
                                                "currency_code": "CAD",
                                                "value": "266.20",
                                            },
                                            "exchange_rate": {
                                                "source_currency": "USD",
                                                "target_currency": "CAD",
                                                "value": "1.37288780487805",
                                            },
                                        },
                                        "links": [
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2D909796HK759514R",  # noqa
                                                "rel": "self",
                                                "method": "GET",
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/payments/captures/2D909796HK759514R/refund",  # noqa
                                                "rel": "refund",
                                                "method": "POST",
                                            },
                                            {
                                                "href": "https://api.sandbox.paypal.com/v2/checkout/orders/6DL65867YS292100Y",  # noqa
                                                "rel": "up",
                                                "method": "GET",
                                            },
                                        ],
                                        "create_time": "2025-04-11T21:53:08Z",
                                        "update_time": "2025-04-11T21:53:08Z",
                                    }
                                ]
                            },
                        }
                    ],
                    "payer": {
                        "name": {"given_name": "John", "surname": "Doe"},
                        "email_address": "lender@mcf.com",
                        "payer_id": "TAE6M66KTEVRW",
                        "address": {"country_code": "US"},
                    },
                    "links": [
                        {
                            "href": "https://api.sandbox.paypal.com/v2/checkout/orders/6DL65867YS292100Y",  # noqa
                            "rel": "self",
                            "method": "GET",
                        }
                    ],
                },
                response_only=True,
            )
        ],
    )
    def get(self, request):
        """Capture PayPal Payment."""
        try:
            token = request.GET.get("token")
            paypal_payment_capture_data = paypal_payment_capture(
                payment_id=token,
                capture_payment_func=lender_make_payment,
            )
            return Response(paypal_payment_capture_data)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


@extend_schema_serializer(component_name="CancelPayPalPayment")
class CancelPayPalPaymentView(APIView):
    """Cancel PayPal Payment View."""

    class InputSerializer(serializers.Serializer):
        """Cancel PayPal Payment Input."""

        paymentId = serializers.CharField(
            help_text="The PayPal payment ID to cancel."
        )

    class OutputSerializer(serializers.Serializer):
        """Cancel PayPal Payment Output."""

        message = serializers.CharField()

    @extend_schema(
        request=InputSerializer,
        parameters=[
            OpenApiParameter(
                name="paymentId",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="The PayPal payment ID to cancel.",
            ),
        ],
        responses={
            200: OutputSerializer,
            400: OpenApiResponse(description="Cancel failed or bad request."),
            404: OpenApiResponse(description="Payment not found."),
        },
        examples=[
            OpenApiExample(
                name="Successful Cancel",
                value={"message": "Payment canceled."},
                response_only=True,
            ),
        ],
    )
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


@extend_schema_serializer(component_name="CapturePayPalPayout")
class CapturePayPalPayoutView(APIView):
    """Capture PayPal Payout View."""

    class InputSerializer(serializers.Serializer):
        """Input for PayPal Payout."""

        payee_id = serializers.IntegerField(
            help_text="The ID of the payee user."
        )
        amount = serializers.CharField(help_text="The amount to be paid out.")

    class OutputSerializer(serializers.Serializer):
        """Output for PayPal Payout."""

        batch_header = serializers.DictField(
            help_text="PayPal payout batch header."
        )

    @extend_schema(
        request=InputSerializer,
        responses={
            200: OutputSerializer,
            400: OpenApiResponse(
                description="Invalid input or payout failed."
            ),
        },
        examples=[
            OpenApiExample(
                name="Valid Request",
                value={"payee_id": 1, "amount": "25.00"},
                request_only=True,
            ),
            OpenApiExample(
                name="Valid Response",
                value={"batch_header": {"payout_batch_id": "XYZ123"}},
                response_only=True,
            ),
        ],
    )
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
