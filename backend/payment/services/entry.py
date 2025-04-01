"""Payment Entry services."""

from django.contrib.auth import get_user_model
from django.db import transaction

from hordak.models import Transaction
from typing import Optional, Callable

from core.services import Amount, to_money
from ..models import Payment, PaymentPlatform, PaymentStatus

User = get_user_model()


def external_payment_create(
    *,
    payer: User,
    gateway_payment_id: str,
    amount: Amount,
    platform: Optional[PaymentPlatform] = PaymentPlatform.PAYPAL,
    status: Optional[PaymentStatus] = PaymentStatus.PENDING,
) -> Payment:
    """Create payment."""
    amount = to_money(amount)
    payment = Payment(
        user=payer,
        gateway_payment_id=gateway_payment_id,
        amount=amount,
        platform=platform,
        status=status,
    )
    payment.full_clean()
    payment.save()

    return payment


@transaction.atomic
def external_payment_capture(
    payment: Payment,
    capture_payment_func: Callable[[User, Amount], Transaction],
) -> Payment:
    """Capture payment."""
    payment.status = PaymentStatus.COMPLETED
    payment.transaction = capture_payment_func(payment.user, payment.amount)
    payment.full_clean()
    payment.save()

    return payment
