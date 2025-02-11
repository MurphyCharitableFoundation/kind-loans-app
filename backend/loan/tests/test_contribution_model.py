"""Tests for contribution model."""

from django.test import TestCase
from djmoney.money import Money
from loan.helpers import create_user_with_group, make_contribution
from loan.models import LoanProfile


class ContributionModelTests(TestCase):
    """Test Contribution Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = create_user_with_group(
            email="borrower@example.com",
            password=password,
            group_name="borrower",
        )
        self.borrower_target_100 = LoanProfile.objects.create(
            user=self.borrower_user,
            profile_img="www.example.com/photo.jpg",
            description="loan profile 1",
            loan_duration=12,
            target_amount=Money(100, "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender = create_user_with_group(
            email="lender@example.com",
            password=password,
            group_name="lender",
            amount_available=Money(50, "USD"),
        )

    def test_lender_can_contribute_to_borrower(self):
        """
        Test that a lender can contribute to loan_profile
        """
        initial_amount_available = self.lender.amount_available
        amount_contributed = Money(25, "USD")

        contribution = make_contribution(
            self.lender, self.borrower_target_100, Money(25, "USD")
        )
        self.assertEqual(self.lender, contribution.lender)
        self.assertEqual(self.borrower_target_100, contribution.borrower)
        self.assertEqual(
            self.lender.amount_available,
            initial_amount_available - amount_contributed,
        )
