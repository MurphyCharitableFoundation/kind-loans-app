"""Payment models."""

from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

from djmoney.money import Money
from djmoney.models.fields import MoneyField
from hordak.models import Transaction
from model_utils.models import TimeStampedModel


class PaymentStatus(models.TextChoices):
    """Transaction Status choices."""

    PENDING = "PENDING", "Pending"  # Payment initiated but not yet processed
    COMPLETED = "COMPLETED", "Completed"  # Payment successfully completed
    FAILED = "FAILED", "Failed"  # Payment attempt failed
    REFUNDED = "REFUNDED", "Refunded"  # Payment was refunded
    CANCELED = (
        "CANCELED",
        "Canceled",
    )  # Payment was canceled by the user or system
    ON_HOLD = "ON_HOLD", "On Hold"  # Payment is temporarily on hold
    CHARGEBACK = "CHARGEBACK", "Chargeback"  # Disputed payment


class PaymentMethod(models.TextChoices):
    """Payment Method choices."""

    CREDIT_CARD = "CREDIT_CARD", "Credit Card"
    DEBIT_CARD = "DEBIT_CARD", "Debit Card"
    PAYPAL = "PAYPAL", "PayPal"
    APPLE_PAY = "APPLE_PAY", "Apple Pay"
    GOOGLE_PAY = "GOOGLE_PAY", "Google Pay"
    BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
    CASH = "CASH", "Cash"
    CRYPTOCURRENCY = "CRYPTOCURRENCY", "Cryptocurrency"


class PaymentPlatform(models.TextChoices):
    """Payment Platform choices."""

    PAYPAL = "PAYPAL", "PayPal"
    STRIPE = "STRIPE", "Stripe"
    OTHER = "OTHER", "Other"


class Payment(TimeStampedModel):
    """Represent a Payment from a number of 3rd Party Platforms."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="payments",
        help_text="The user who initiated the payment.",
    )
    platform = models.CharField(
        max_length=20,
        default=PaymentPlatform.PAYPAL,
        choices=PaymentPlatform.choices,
        help_text="The external payment platform used.",
    )
    gateway_payment_id = models.CharField(max_length=255, unique=True)
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
        related_name="payment",
        null=True,
        blank=True,
    )
    amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text="The status of the payment.",
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-created"]

    def __str__(self):
        """Represent Payment as str."""
        return "Payment: {} payment by {} - {}".format(
            self.platform, self.user, self.gateway_payment_id
        )
