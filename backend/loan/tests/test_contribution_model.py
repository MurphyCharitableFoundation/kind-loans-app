"""Tests for contribution model."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from loan import helpers, models


class ContributionModelTests(TestCase):
    """Test Contribution Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = get_user_model().objects.create_user(
            email="borrower@example.com", password=password
        )
        self.borrower_target_100 = models.LoanProfile.objects.create(
            user=self.borrower_user,
            profile_img="www.example.com/photo.jpg",
            description="loan profile 1",
            loan_duration=12,
            target_amount=Money(100, "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender = get_user_model().objects.create_user(
            email="lender@example.com",
            password=password,
            role=models.UserRole.LENDER,
            amount_available=Money(50, "USD"),
        )

    def test_lender_can_contribute_to_borrower(self):
        """
        Test that a lender can contribute to loan_profile
        """
        initial_amount_available = self.lender.amount_available
        amount_contributed = Money(25, "USD")

        contribution = helpers.make_contribution(
            self.lender, self.borrower_target_100, Money(25, "USD")
        )
        self.assertEqual(self.lender, contribution.lender)
        self.assertEqual(self.borrower_target_100, contribution.loan_profile)
        self.assertEqual(
            self.lender.amount_available,
            initial_amount_available - amount_contributed,
        )
