"""Contribution Services."""

from core.services import Amount, to_money
from django.contrib.auth import get_user_model
from django.db import transaction

from ..models import Contribution, LoanProfile

User = get_user_model()


@transaction.atomic
def contribution_create(
    *,
    lender: User,
    borrower: LoanProfile,
    amount: Amount,
) -> Contribution:
    """
    Create Contribution.

    Cap contribution amount at borrower's remaining need.
    """
    amount = to_money(amount)

    remaining_need = borrower.target_amount - borrower.total_raised()

    if amount > remaining_need:
        amount = remaining_need

    contribution = Contribution(
        lender=lender, borrower=borrower, amount=amount
    )
    contribution.full_clean()
    contribution.save()

    lender.amount_available -= amount
    lender.full_clean()
    lender.save()

    return contribution
