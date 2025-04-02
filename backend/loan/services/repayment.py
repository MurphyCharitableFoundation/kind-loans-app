"""Repayment Services."""

from typing import Optional

from core.services import Amount, to_money
from django.contrib.auth import get_user_model
from django.db import transaction

from ..models import LoanProfile, Repayment

User = get_user_model()


@transaction.atomic
def repayment_create(
    *,
    borrower: LoanProfile,
    amount: Amount,
    description: Optional[str] = None,
) -> Repayment:
    """
    Create Repayment Entry.

    Caps amount at Loan Profile's remaining balance.
    """
    amount = to_money(amount)
    remaining_balance = borrower.remaining_balance()

    if amount > remaining_balance:
        amount = remaining_balance

    repayment = Repayment(
        borrower=borrower, amount=amount, description=description
    )
    repayment.full_clean()
    repayment.save()

    return repayment


@transaction.atomic
def repayment_apply(*, repayment: Repayment) -> None:
    """Apply Repayment to lenders based on their contributions."""
    from .contribution import Contribution

    if not repayment.is_applied:

        def repay_lender_by_contribution(contribution: Contribution) -> None:
            def cut():
                """BUG: off by 1 cent in some cases."""
                return to_money(
                    repayment.amount.amount
                    * contribution.amount.amount
                    / repayment.borrower.total_raised().amount
                )

            lender = contribution.lender
            lender.amount_available += cut()
            lender.save()

        for contribution in repayment.borrower.contributions.all():
            repay_lender_by_contribution(contribution)

        repayment.is_applied = True
        repayment.save()
