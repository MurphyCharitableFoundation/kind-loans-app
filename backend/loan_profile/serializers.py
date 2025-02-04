"""
Serializers for the loan_profile app.
"""

from rest_framework import serializers
from core.models import LoanProfile

from djmoney.contrib.django_rest_framework.fields import MoneyField


class LoanProfileSerializer(serializers.ModelSerializer):
    """Serializer for loan profile objects."""

    user_name = serializers.CharField(source="user.name", read_only=True)
    total_amount_required = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD"
    )

    class Meta:
        model = LoanProfile
        fields = (
            "id",
            "user",
            "user_name",
            "title",
            "status",
            "photoURL",
            "categories",
            "loan_duration_months",
            "total_amount_required",
        )
        read_only_fields = (
            "id",
            "user",
            "status",
            "user_name",
        )


class LoanProfileDetailSerializer(LoanProfileSerializer):
    """Serializer for loan profile detail objects."""

    user_name = serializers.CharField(source="user.name", read_only=True)
    total_amount_required = MoneyField(
        max_digits=10, decimal_places=2, default_currency="USD"
    )

    class Meta:
        model = LoanProfile
        fields = LoanProfileSerializer.Meta.fields + (
            "description",
            "deadline_to_receive_loan",
            "user_name",
        )
        read_only_fields = ("id", "user", "status", "user_name")
