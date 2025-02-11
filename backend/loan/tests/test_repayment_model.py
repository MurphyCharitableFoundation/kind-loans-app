"""Tests for models."""

from django.test import TestCase
from djmoney.money import Money
from loan.helpers import (create_user_with_group, make_contribution,
                          make_repayment)
from loan.models import LoanProfile


class RepaymentModelTests(TestCase):
    """Test Repayment Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = create_user_with_group(
            email="borrower@example.com",
            password=password,
            group_name="borrower",
        )
        self.borrower_target_100_repaid_50 = LoanProfile.objects.create(
            user=self.borrower_user,
            profile_img="www.example.com/photo.jpg",
            description="loan profile 1",
            loan_duration=12,
            target_amount=Money(100, "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender_a = create_user_with_group(
            email="lenderA@example.com",
            password=password,
            group_name="lender",
            amount_available=Money(50, "USD"),
        )

        self.lender_b = create_user_with_group(
            email="lenderB@example.com",
            password=password,
            group_name="lender",
            amount_available=Money(50, "USD"),
        )

        self.contribution_a = make_contribution(
            self.lender_a, self.borrower_target_100_repaid_50, Money(50, "USD")
        )

        self.contribution_b = make_contribution(
            self.lender_b, self.borrower_target_100_repaid_50, Money(50, "USD")
        )

    def test_borrower_can_make_single_repayment(self):
        """
        Test that a lender can contribute to loan_profile
        """
        repayment_amount = Money(50, "USD")
        repayment = make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount
        )

        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment.borrower
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
        repayment_a = make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount_a
        )
        repayment_b = make_repayment(
            self.borrower_target_100_repaid_50, repayment_amount_b
        )

        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment_a.borrower
        )
        self.assertEqual(repayment_amount_a, repayment_a.amount)
        self.assertEqual(
            self.borrower_target_100_repaid_50, repayment_b.borrower
        )
        self.assertEqual(repayment_amount_b, repayment_b.amount)
        self.assertEqual(
            self.borrower_target_100_repaid_50.repayments.count(), 2
        )
