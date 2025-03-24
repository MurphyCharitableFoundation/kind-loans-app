"""Lender services."""

from django.contrib.auth import get_user_model

from hordak.models import Transaction
from core.services import Amount, to_money


User = get_user_model()


def lender_make_payment(lender: User, amount: Amount) -> Transaction:
    """Lender pays money to MCF."""
    return lender.purchase_credits(to_money(amount))


def lender_receive_payment(lender: User, amount: Amount) -> Transaction:
    """Lender withdraws money from MCF."""
    return lender.withdraw_credits(to_money(amount))
