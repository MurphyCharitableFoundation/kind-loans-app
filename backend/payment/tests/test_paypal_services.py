from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from payment.services import (
    paypal_payment_create,
    paypal_payment_capture,
    paypal_payout_create,
)


User = get_user_model()


class PayPalServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="pass"
        )
        self.amount = "10.00"

    @patch("payment.services.paypal.external_payment_create")
    @patch("payment.services.paypal.requests.post")
    def test_paypal_payment_create_success(
        self, mock_post, mock_external_create
    ):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"id": "PAYPAL_ORDER_ID"}

        result = paypal_payment_create(
            payer=self.user,
            amount=self.amount,
            return_url="http://test/return",
            cancel_url="http://test/cancel",
        )

        self.assertEqual(result["id"], "PAYPAL_ORDER_ID")
        mock_external_create.assert_called_once_with(
            payer=self.user,
            amount=self.amount,
            gateway_payment_id="PAYPAL_ORDER_ID",
        )

    @patch("payment.services.paypal.external_payment_capture")
    @patch("payment.services.paypal.payment_get")
    @patch("payment.services.paypal.requests.post")
    def test_paypal_payment_capture_success(
        self, mock_post, mock_payment_get, mock_external_capture
    ):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "COMPLETED"}

        mock_payment = MagicMock()
        mock_payment_get.return_value = mock_payment

        def fake_capture(user, amount):
            return "ok"

        result = paypal_payment_capture(
            payment_id="PAYPAL_ORDER_ID", capture_payment_func=fake_capture
        )

        self.assertEqual(result["status"], "COMPLETED")
        mock_external_capture.assert_called_once_with(
            payment=mock_payment, capture_payment_func=fake_capture
        )

    @patch("payment.services.paypal.requests.post")
    def test_paypal_payout_create_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "batch_header": {"payout_batch_id": "XYZ123"}
        }

        def fake_capture(user, amount):
            return "ok"

        result = paypal_payout_create(
            user=self.user,
            amount="25.00",
            capture_payout_func=fake_capture,
        )

        self.assertIn("batch_header", result)
        self.assertEqual(result["batch_header"]["payout_batch_id"], "XYZ123")
