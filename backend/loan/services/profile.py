"""Loan Profile Services."""

from datetime import date
from typing import List, Optional

from accounting.operations import app_to_borrower, borrower_to_app
from core.services import Amount, to_money
from django.contrib.auth import get_user_model
from django.db import transaction
from hordak.models import Transaction

from ..models import Category, LoanProfile, LoanProfileStatus, Repayment
from ..utils import one_year_from_now_date

User = get_user_model()

DEFAULT_LOAN_DURATION = 12  # 12 months


def category_create(*, name: str) -> Category:
    """Create Category."""
    category, _ = Category.objects.get_or_create(name=name)

    return category


@transaction.atomic
def loan_profile_create(
    *,
    user: User,
    title: str,
    target_amount: Amount,
    loan_duration: Optional[int] = DEFAULT_LOAN_DURATION,
    profile_img: Optional[str] = None,
    deadline_to_receive_loan: Optional[date] = one_year_from_now_date(),
    status: Optional[str] = LoanProfileStatus.PENDING,
    city: Optional[str] = None,
    country: Optional[str] = None,
    description: Optional[str] = None,
    story: Optional[str] = None,
    category_names: Optional[List[str]] = None,
) -> LoanProfile:
    """Create Loan Profile."""
    target_amount = to_money(target_amount)
    loan_profile = LoanProfile(
        user=user,
        title=title,
        profile_img=profile_img,
        description=description,
        story=story,
        status=status,
        target_amount=target_amount,
        loan_duration=loan_duration,
        deadline_to_receive_loan=deadline_to_receive_loan,
        city=city,
        country=country,
    )
    loan_profile.full_clean()
    loan_profile.save()

    if category_names:
        for name in category_names:
            category = category_create(name=name)
            loan_profile.categories.add(category)

    return loan_profile


@transaction.atomic
def borrower_receive_payment(borrower: LoanProfile) -> Transaction:
    """Borrower receive payment of total-raised-amount from MCF."""
    borrower.is_paid_raised_amount = True
    borrower.full_clean()
    borrower.save()

    return app_to_borrower(borrower, borrower.total_raised())


@transaction.atomic
def borrower_make_payment(borrower: LoanProfile) -> Transaction:
    """Borrower make payment of total-repaid-amount to MCF."""
    borrower.has_repaid = True
    borrower.full_clean()
    borrower.save()

    return borrower_to_app(
        borrower, borrower.total_repaid(), borrower.remaining_balance()
    )


def borrower_enter_repayment(
    *,
    borrower: LoanProfile,
    amount: Amount,
) -> Repayment:
    """For given loan_profile, repay amount."""
    from .repayment import repayment_create

    return repayment_create(borrower=borrower, amount=amount)


def borrower_apply_repayments(*, borrower: LoanProfile) -> None:
    """For borrower, apply all repayments to lenders."""
    from .repayment import repayment_apply

    repayments = borrower.repayments.all()
    return list(
        map(lambda repayment: repayment_apply(repayment=repayment), repayments)
    )
