"""Tests for contribution model."""

from django.test import TestCase
from djmoney.money import Money

from ..services import contribution_create, loan_profile_create, user_create


class ContributionModelTests(TestCase):
    """Test Contribution Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = user_create(
            email="borrower@example.com",
            password=password,
            group_name="borrower",
        )
        self.borrower_target_100 = loan_profile_create(
            user=self.borrower_user,
            profile_img="https://www.example.com/photo.jpg",
            title="loan profile 1",
            description="loan profile 1",
            loan_duration=12,
            target_amount=Money(100, "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender = user_create(
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

        contribution = contribution_create(
            lender=self.lender, borrower=self.borrower_target_100, amount=25
        )
        self.assertEqual(self.lender, contribution.lender)
        self.assertEqual(self.borrower_target_100, contribution.borrower)
        self.assertEqual(
            self.lender.amount_available,
            initial_amount_available - amount_contributed,
        )
