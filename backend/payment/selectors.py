"""Payment selectors."""

from typing import Optional

from core.utils import get_object
from django.db.models.query import QuerySet

from .filters import PaymentFilter
from .models import Payment


def payment_get(
    *,
    payment_id: Optional[int] = None,
    payment_gateway_id: Optional[str] = None,
) -> Optional[Payment]:
    """Retrieve Payment."""
    if payment_id:
        return get_object(Payment, id=payment_id)
    elif payment_gateway_id:
        return get_object(Payment, payment_gateway_id=payment_gateway_id)

    return None


# TODO: filtering untested
def payment_list(*, filters=None) -> QuerySet[Payment]:
    """Retrieve Payments."""
    filters = filters or {}
    qs = Payment.objects.all()
    return PaymentFilter(filters, qs).qs
