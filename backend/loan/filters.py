"""Loan filters."""

import django_filters

from .models import Contribution, LoanProfile, Repayment


class LoanProfileFilter(django_filters.FilterSet):
    """LoanProfile Filter."""

    class Meta:
        model = LoanProfile
        fields = (
            "id",
            "user",
            "title",
            "description",
            "story",
            "loan_duration",
            "target_amount",
            "is_paid_raised_amount",
            "has_repaid",
            "status",
            "categories",
            "country",
            "city",
            "created",
            "modified",
        )


class ContributionFilter(django_filters.FilterSet):
    """Contribution Filter."""

    class Meta:
        model = Contribution
        fields = (
            "id",
            "lender",
            "borrower",
            "amount",
            "created",
            "modified",
        )


class RepaymentFilter(django_filters.FilterSet):
    """Repayment Filter."""

    class Meta:
        model = Repayment
        fields = (
            "id",
            "borrower",
            "amount",
            "description",
            "is_applied",
            "created",
            "modified",
        )
