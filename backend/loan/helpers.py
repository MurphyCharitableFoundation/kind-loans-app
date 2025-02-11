"""Helpers for Loan app."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db import transaction

from .validators import (
    validate_contribution_amount,
    validate_contribution_amount_from_lender,
    validate_repayment_amount,
)

User = get_user_model()


def make_payment(lender, amount, **kwargs):
    """Create a payment for in-app credits."""
    return lender.purchase_credits(amount)


def make_payout(lender, amount, **kwargs):
    """Create a payout from in-app credits."""
    return lender.withdraw_credits(amount)


def make_contribution(lender, borrower, amount, **kwargs):
    """
    Create a contribution, validate and raise errors.

    :param lender: Lender instance
    :param borrower: Borrower instance
    :param amount: Money object representing contribution amount
    :param kwargs: Additional fields to pass to Contribution model
    :return: Created Contribution instance
    :raises ValidationError: If contribution is invalid
    """
    from .models import Contribution  # Import here to avoid circular imports

    try:
        # Validate contribution amount
        remaining_need = borrower.target_amount - borrower.total_raised()

        if amount > remaining_need:
            amount = remaining_need  # Cap contribution at remaining need

        validate_contribution_amount(borrower, amount)
        validate_contribution_amount_from_lender(lender, amount)

        # Use transaction to ensure atomic creation
        with transaction.atomic():
            lender.amount_available -= amount
            lender.save()

            contribution = Contribution.objects.create(
                lender=lender, borrower=borrower, amount=amount, **kwargs
            )

        return contribution

    except Exception as e:
        raise ValidationError(f"Contribution failed: {str(e)}")


def make_repayment(borrower, amount, **kwargs):
    """
    Create a repayment, validate and raise errors.

    :param borrower: Borrower instance
    :param amount: Money object representing repayment amount
    :param kwargs: Additional fields to pass to Repayment model
    :return: Created Repayment instance
    :raises ValidationError: If repayment is invalid
    """
    from .models import Repayment  # Import here to avoid circular imports

    try:
        # Validate repayment amount
        remaining_balance = borrower.remaining_balance()

        if amount > remaining_balance:
            amount = remaining_balance  # Cap repayment at remaining balance

        validate_repayment_amount(borrower, amount)

        # Use transaction to ensure atomic creation
        with transaction.atomic():
            repayment = Repayment.objects.create(
                borrower=borrower, amount=amount, **kwargs
            )

        return repayment

    except Exception as e:
        raise ValidationError(f"Repayment failed: {str(e)}")


def create_user_with_group(
    email: str, password: str, group_name: str, **kwargs
) -> User:
    """
    Create a user given email and password, assigns them to a group.

    - The group name is **case-insensitive** and is always stored in lowercase.
    - If the group does not exist,
      it will be created **only if it's in the allowed list**.
    - If the group is not in the allowed list, it will be ignored.

    Allowed groups: ["admin", "lender", "borrower"]
    """
    allowed_groups = {"admin", "lender", "borrower"}

    # Normalize group name (case-insensitive, lowercase)
    normalized_group_name = group_name.lower()

    user = User.objects.create_user(email=email, password=password, **kwargs)

    if normalized_group_name in allowed_groups:
        group, _ = Group.objects.get_or_create(name=normalized_group_name)
        user.groups.add(group)

    return user
