"""Test PayPal Views."""

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from unittest.mock import patch


User = get_user_model()


class PayPalViewsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com", password="pass"
        )
        self.client.force_authenticate(user=self.user)

    @patch("payment.views.paypal_payment_create")
    @patch("payment.views.reverse")
    def test_create_paypal_payment_view(
        self, mock_reverse, mock_create_payment
    ):
        mock_create_payment.return_value = {"id": "PAYPAL_ORDER_123"}

        # Fake reverse URLs to avoid NoReverseMatch during the test
        mock_reverse.side_effect = lambda name, args=None: (
            f"/mocked/{name}/{args[0]}/" if args else f"/mocked/{name}/"
        )

        url = reverse("paypal-create")
        data = {
            "amount": "20.00",
            "currency": "USD",
            "payer_id": self.user.id,
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["id"], "PAYPAL_ORDER_123")
        mock_create_payment.assert_called_once()

    @patch("payment.views.paypal_payment_capture")
    def test_capture_paypal_payment_view(self, mock_capture_payment):
        mock_capture_payment.return_value = {"status": "COMPLETED"}

        def fake_capture(user, amount):
            return "ok"

        # Patch the function used in the view to avoid mismatch
        with patch("payment.views.lender_make_payment", new=fake_capture):
            url = reverse("paypal-capture", args=["ORDER123"])
            response = self.client.get(url)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["status"], "COMPLETED")
            mock_capture_payment.assert_called_once_with(
                payment_id="ORDER123", capture_payment_func=fake_capture
            )

    @patch("payment.views.paypal_payout_create")
    def test_capture_paypal_payout_view(self, mock_payout_create):
        mock_payout_create.return_value = {
            "batch_header": {"payout_batch_id": "XYZ"}
        }

        url = reverse("paypal-payout")
        data = {"amount": "15.00"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["batch_header"]["payout_batch_id"], "XYZ"
        )
        mock_payout_create.assert_called_once()
