"""Donation selectors."""

from typing import Optional

from core.utils import get_object
from django.db.models.query import QuerySet

from ..filters import ContributionFilter
from ..models import Contribution


def contribution_get(contribution_id) -> Optional[Contribution]:
    """Retrieve Contribution."""
    contribution = get_object(Contribution, id=contribution_id)

    return contribution


# TODO: filtering untested
def contribution_list(*, filters=None) -> QuerySet[Contribution]:
    """Retrieve Contributions."""
    filters = filters or {}
    qs = Contribution.objects.all()
    return ContributionFilter(filters, qs).qs
