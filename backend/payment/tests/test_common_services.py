"""Test common services."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from hordak.models import Transaction

from payment.models import Payment, PaymentStatus, PaymentPlatform
from payment.services.common import (
    external_payment_create,
    external_payment_capture,
)
from core.services import to_money


User = get_user_model()


class ExternalPaymentServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", password="pass"
        )
        self.amount = "25.00"
        self.gateway_payment_id = "PAYPAL123"

    def test_external_payment_create_creates_payment(self):
        payment = external_payment_create(
            payer=self.user,
            gateway_payment_id=self.gateway_payment_id,
            amount=self.amount,
        )

        self.assertIsInstance(payment, Payment)
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.gateway_payment_id, self.gateway_payment_id)
        self.assertEqual(payment.amount, to_money(self.amount))
        self.assertEqual(payment.status, PaymentStatus.PENDING)
        self.assertEqual(payment.platform, PaymentPlatform.PAYPAL)

    def test_external_payment_capture_marks_payment_completed(
        self,
    ):
        """
        Test payment capture marks payment complete and links transaction.
        """
        # First create the payment
        payment = external_payment_create(
            payer=self.user,
            gateway_payment_id=self.gateway_payment_id,
            amount=self.amount,
        )

        # Create a mock transaction object
        fake_transaction = Transaction.objects.create()

        def fake_capture(user, amount):
            return fake_transaction

        updated_payment = external_payment_capture(
            payment=payment, capture_payment_func=fake_capture
        )

        self.assertEqual(updated_payment.status, PaymentStatus.COMPLETED)
        self.assertEqual(updated_payment.transaction, fake_transaction)
