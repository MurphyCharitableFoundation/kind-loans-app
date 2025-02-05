"""Tests for models."""

from core import models
from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money


class LoanProfileModelTests(TestCase):
    """Test user model"""

    def test_create_loan_profile(self):
        """Test creating a new loan profile"""
        user = get_user_model().objects.create_user(
            "test@example.com", "testpass123"
        )
        loan_profile = models.LoanProfile.objects.create(
            user=user,
            profile_img="www.example.com/photo.jpg",
            title="Test title",
            description="Test description",
            loan_duration=12,
            target_amount=Money("500.00", "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )
        self.assertEqual(
            str(loan_profile),
            f"{loan_profile.title} by {user.first_name} {user.last_name}",
        )
