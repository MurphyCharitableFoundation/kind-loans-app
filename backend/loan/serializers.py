from djmoney.contrib.django_rest_framework.fields import MoneyField
from rest_framework import serializers

from .models import Category, LoanProfile


class LoanProfileSerializer(serializers.ModelSerializer):
    target_amount = MoneyField(max_digits=12, decimal_places=2)
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
            "is_paid_raised_amount",
            "has_repaid",
            "categories",
            "modified",
        ]
        read_only_fields = [
            "user",
            "modified",
            "has_repaid",
            "deadline_to_receive_loan",
            "is_paid_raised_amount",
            "loan_duration",
        ]

    def create(self, validated_data):
        """Handle category creation properly during LoanProfile creation."""
        categories_data = validated_data.pop("categories", [])
        loan_profile = LoanProfile.objects.create(**validated_data)

        # Add categories if provided
        for category in categories_data:
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
