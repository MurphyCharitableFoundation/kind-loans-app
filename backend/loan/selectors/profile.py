"""Loan profile selectors."""

from typing import Optional

from core.utils import get_object
from django.db.models.query import QuerySet

from ..filters import LoanProfileFilter
from ..models import LoanProfile


def loan_profile_get(loan_profile_id) -> Optional[LoanProfile]:
    """Retrieve Loan Profile."""
    lp = get_object(LoanProfile, id=loan_profile_id)

    return lp


# TODO: filtering untested
def loan_profile_list(*, filters=None) -> QuerySet[LoanProfile]:
    """Retrieve Contributions."""
    filters = filters or {}
    qs = LoanProfile.objects.all()
    return LoanProfileFilter(filters, qs).qs
