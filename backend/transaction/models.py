from django.conf import settings
from django.db import models
from model_utils.models import TimeStampedModel
from hordak.models import Transaction
from djmoney.models.fields import MoneyField


class TransactionStatus(models.IntegerChoices):
    """Transaction Status choices."""

    PENDING = 1, "Pending"  # Payment initiated but not yet processed
    COMPLETED = 2, "Completed"  # Payment successfully completed
    FAILED = 3, "Failed"  # Payment attempt failed
    REFUNDED = 4, "Refunded"  # Payment was refunded
    CANCELED = 5, "Canceled"  # Payment was canceled by the user or system
    ON_HOLD = 6, "On Hold"  # Payment is temporarily on hold
    CHARGEBACK = 7, "Chargeback"  # Disputed payment


class PaymentMethod(models.IntegerChoices):
    """Payment Method choices."""

    CREDIT_CARD = 1, "Credit Card"
    DEBIT_CARD = 2, "Debit Card"
    PAYPAL = 3, "PayPal"
    APPLE_PAY = 4, "Apple Pay"
    GOOGLE_PAY = 5, "Google Pay"
    BANK_TRANSFER = 6, "Bank Transfer"
    CASH = 7, "Cash"
    CRYPTOCURRENCY = 9, "Cryptocurrency"


class ExternalPayment(TimeStampedModel):
    PAYMENT_STATUSES = [
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("CANCELLED", "Cancelled"),
    ]

    PLATFORM_CHOICES = [
        ("PAYPAL", "PayPal"),
        ("STRIPE", "Stripe"),
        ("OTHER", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="external_payments",
        help_text="The user who initiated the payment.",
    )
    platform = models.CharField(
        max_length=20,
        default="PAYPAL",
        choices=PLATFORM_CHOICES,
        help_text="The external payment platform used.",
    )
    gateway_payment_id = models.CharField(max_length=255, unique=True)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="external_payment",
        null=True,
        blank=True,
    )
    amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUSES,
        default="PENDING",
        help_text="The status of the payment.",
    )

    class Meta:
        verbose_name = "External Payment"
        verbose_name_plural = "External Payments"
        ordering = ["-created"]

    def __str__(self):
        return (
            f"{self.platform} payment by {self.user} - {self.transaction_id}"
        )

    def mark_as_completed(self):
        self.status = "COMPLETED"
        self.save()

    def mark_as_failed(self):
        self.status = "FAILED"
        self.save()
