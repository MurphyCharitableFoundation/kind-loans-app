"""Loan serializers."""

from djmoney.contrib.django_rest_framework.fields import MoneyField
from rest_framework import serializers

from .models import Category, LoanProfile
from .services import category_create, loan_profile_create


class LoanProfileSerializer(serializers.ModelSerializer):
    target_amount = MoneyField(max_digits=12, decimal_places=2)
    total_raised = MoneyField(max_digits=12, decimal_places=2, read_only=True)
    total_repaid = MoneyField(max_digits=12, decimal_places=2, read_only=True)
    remaining_balance = MoneyField(
        max_digits=12, decimal_places=2, read_only=True
    )
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Category.objects.all(),
        required=False,
    )

    class Meta:
        model = LoanProfile
        fields = [
            "id",
            "user",
            "title",
            "description",
            "story",
            "profile_img",
            "loan_duration",
            "deadline_to_receive_loan",
            "target_amount",
            "total_raised",
            "total_repaid",
            "remaining_balance",
            "is_paid_raised_amount",
            "has_repaid",
            "categories",
            "country",
            "city",
            "created",
            "modified",
        ]
        read_only_fields = [
            "user",
            "modified",
            "has_repaid",
            "deadline_to_receive_loan",
            "is_paid_raised_amount",
            "loan_duration",
            "total_raised",
            "total_repaid",
            "remaining_balance",
        ]

    def create(self, validated_data):
        """Handle category creation properly during LoanProfile creation."""
        categories_data = validated_data.pop("categories", [])
        loan_profile = loan_profile_create(**validated_data)

        # Add categories if provided
        for category in categories_data:
            category = category_create(name=category)
            loan_profile.categories.add(category)

        return loan_profile

    def update(self, instance, validated_data):
        """Allow updates but ensure category handling is correct."""
        categories_data = validated_data.pop("categories", None)

        instance = super().update(instance, validated_data)

        if categories_data is not None:
            instance.categories.set(
                categories_data
            )  # Replace categories if provided

        return instance
