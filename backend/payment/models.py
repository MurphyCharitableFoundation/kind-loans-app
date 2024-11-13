from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError

from model_utils.models import TimeStampedModel


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


class TransactionManager(models.Manager):
    """Manager for transactions."""

    def create_transaction(
        self, payer, recipient, payment_id, amount, **extra_fields
    ):
        """Create, save, and return a new transaction."""
        payer_content_type = ContentType.objects.get_for_model(payer)
        recipient_content_type = ContentType.objects.get_for_model(recipient)

        transaction = self.model(
            payer_content_type=payer_content_type,
            payer_object_id=payer.id,
            recipient_content_type=recipient_content_type,
            recipient_object_id=recipient.id,
            amount=amount,
            payment_id=payment_id,
            **extra_fields,
        )
        transaction.save(using=self._db)

        return transaction

    def amount_received(self, entity):
        entity_content_type = ContentType.objects.get_for_model(entity)

        result = self.filter(
            recipient_content_type=entity_content_type,
            recipient_object_id=entity.id,
            status=TransactionStatus.COMPLETED,
        ).aggregate(total=models.Sum("amount"))

        return result["total"] or 0


# TODO:
# + currency
# + on-delete: transactions cannot be deleted for audit reasons
#   instead prevent delete on user object or loanprofile, resort to
#   hiding/making inactive
class Transaction(TimeStampedModel):
    """Transaction model."""

    payer_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="payer_transactions",
    )
    payer_object_id = models.PositiveIntegerField()
    payer = GenericForeignKey("payer_content_type", "payer_object_id")

    recipient_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="recipient_transactions",
    )
    recipient_object_id = models.PositiveIntegerField()
    recipient = GenericForeignKey(
        "recipient_content_type", "recipient_object_id"
    )

    payment_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The amount for the transaction.",
    )
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.PAYPAL,
        help_text="The method of payment for the transaction.",
    )
    status = models.IntegerField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        help_text="The status of the transaction.",
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-created"]

    def __str__(self):
        return f"{self.payer} ----({self.amount})----> {self.recipient}"

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Transaction amount cannot be negative.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Transaction cannot be deleted.")

    def delete_queryset(self, qs, *args, **kwargs):
        raise ValidationError("Bulk deletion is not allowed for Transactions.")
