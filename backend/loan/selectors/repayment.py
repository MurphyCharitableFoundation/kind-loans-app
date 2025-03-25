"""Repayment selectors."""

from typing import Optional

from core.utils import get_object
from django.db.models.query import QuerySet

from ..filters import RepaymentFilter
from ..models import Repayment


def repayment_get(repayment_id) -> Optional[Repayment]:
    """Retrieve Repayment."""
    repayment = get_object(Repayment, id=repayment_id)

    return repayment


# TODO: filtering untested
def repayment_list(*, filters=None) -> QuerySet[Repayment]:
    """Retrieve Repayments."""
    filters = filters or {}
    qs = Repayment.objects.all()
    return RepaymentFilter(filters, qs).qs
