"""Tests for models."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from djmoney.money import Money
from loan import helpers, models


class RepaymentModelTests(TestCase):
    """Test Repayment Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = get_user_model().objects.create_user(
            email="borrower@example.com", password=password
        )
        self.borrower_target_100_repaid_50 = models.LoanProfile.objects.create(
            user=self.borrower_user,
            profile_img="www.example.com/photo.jpg",
            description="loan profile 1",
            loan_duration=12,
            target_amount=Money(100, "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender_a = get_user_model().objects.create_user(
            email="lenderA@example.com",
            password=password,
            role=models.UserRole.LENDER,
            amount_available=Money(50, "USD"),
        )

        self.lender_b = get_user_model().objects.create_user(
            email="lenderB@example.com",
            password=password,
            role=models.UserRole.LENDER,
            amount_available=Money(50, "USD"),
        )

        self.contribution_a = helpers.make_contribution(
            self.lender_a, self.borrower_target_100_repaid_50, Money(50, "USD")
        )

        self.contribution_b = helpers.make_contribution(
            self.lender_b, self.borrower_target_100_repaid_50, Money(50, "USD")
        )

    def test_borrower_can_make_single_repayment(self):
        """
        Test that a lender can contribute to loan_profile
        """
        repayment_amount = Money(50, "USD")
        repayment = helpers.make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount
        )

        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment.loan_profile
        )
        self.assertEqual(repayment_amount, repayment.amount)
        self.assertEqual(
            self.borrower_target_100_repaid_50.repayments.count(), 1
        )

    def test_borrower_can_make_multiple_repayments(self):
        """
        Test that a lender can contribute to loan_profile
        """
        repayment_amount_a = Money(20, "USD")
        repayment_amount_b = Money(30, "USD")
        repayment_a = helpers.make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount_a
        )
        repayment_b = helpers.make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount_b
        )

        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment_a.loan_profile
        )
        self.assertEqual(repayment_amount_a, repayment_a.amount)
        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment_b.loan_profile
        )
        self.assertEqual(repayment_amount_b, repayment_b.amount)
        self.assertEqual(
            self.borrower_target_100_repaid_50.repayments.count(), 2
        )
