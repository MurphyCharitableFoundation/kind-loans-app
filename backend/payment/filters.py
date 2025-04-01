"""Payment filters."""

import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    """Payment Filter."""

    class Meta:
        model = Payment
        fields = (
            "id",
            "user",
            "platform",
            "gateway_payment_id",
            "transaction",
            "amount",
            "status",
            "created",
            "modified",
        )
