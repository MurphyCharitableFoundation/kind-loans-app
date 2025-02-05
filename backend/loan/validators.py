"""Validators for loan app."""

from django.core.exceptions import ValidationError


def validate_repayment_amount(borrower, amount):
    """Validate that repayment amount does not exceed remaining balance."""
    rb = borrower.remaining_balance()

    if amount > rb:
        raise ValidationError(
            f"Repayment amount {amount} > remaining balance {rb}"
        )


def validate_contribution_amount_from_lender(lender, amount):
    """Validate that amount does not exceed lender's available balance."""
    max_contribution = lender.amount_available

    if amount > max_contribution:
        raise ValidationError(
            f"{lender} can contribute maximum of {max_contribution}"
        )


def validate_contribution_amount(borrower, amount):
    """Validate that contribution does not exceed remaining funding need."""
    total_raised = borrower.total_raised()
    rfn = borrower.target_amount - total_raised

    if amount > rfn:
        raise ValidationError(
            f"Contribution amount {amount} > remaining funding need {rfn}"
        )
