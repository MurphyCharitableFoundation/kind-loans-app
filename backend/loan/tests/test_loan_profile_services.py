"""Tests for models."""

from django.conf import settings
from django.test import TestCase
from djmoney.money import Money

from ..services import loan_profile_create, user_create


class LoanProfileModelTests(TestCase):
    """Test loan profile"""

    def test_create_loan_profile(self):
        """Test creating a new loan profile"""
        user = user_create("test@example.com", "testpass123", "borrower")
        loan_profile = loan_profile_create(
            user=user,
            title="Test title",
            description="Test description",
            profile_img="https://www.example.com/photo.jpg",
            loan_duration=12,
            target_amount=Money("500.00", "USD"),
        )
        self.assertEqual(
            str(loan_profile),
            f"Loan Profile: {loan_profile.title} by {user.get_full_name()}",
        )

    def test_create_loan_profile_with_numeric_target_amount(self):
        """Test creating a loan profile with a numeric target amount."""
        user = user_create("test@example.com", "testpass123", "borrower")
        loan_profile = loan_profile_create(
            user=user,
            title="Startup Loan",
            target_amount=15000.00,
            description="Funding for a tech startup.",
            story="This loan will help us develop our product.",
            category_names=["Startup"],
        )

        self.assertEqual(loan_profile.target_amount.amount, 15000.00)
        self.assertEqual(
            loan_profile.target_amount_currency,
            settings.DEFAULT_MONEY_CURRENCY,
        )

    def test_create_loan_profile_without_categories(self):
        """Test creating a loan profile when categories are not provided."""
        user = user_create("test@example.com", "testpass123", "borrower")
        loan_profile = loan_profile_create(
            user=user,
            title="Business Loan",
            target_amount=Money(10000.00, "USD"),
            description="Funding for a startup.",
            story="I need this loan to launch my business.",
        )

        self.assertEqual(loan_profile.categories.count(), 0)

    def test_create_loan_profile_with_categories(self):
        """Test creating a loan profile with categories."""
        user = user_create("test@example.com", "testpass123", "borrower")
        loan_profile = loan_profile_create(
            user=user,
            title="Education Loan",
            target_amount=Money(5000.00, "USD"),
            description="Help me pay tuition fees.",
            story="I need this loan to complete my final semester.",
            category_names=["Education", "Scholarship"],
        )

        self.assertEqual(loan_profile.categories.count(), 2)
