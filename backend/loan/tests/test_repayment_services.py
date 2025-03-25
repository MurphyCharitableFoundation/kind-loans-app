"""Tests for models."""

from django.test import TestCase
from djmoney.money import Money

from ..services import (contribution_create, loan_profile_create,
                        repayment_create, user_create)


class RepaymentModelTests(TestCase):
    """Test Repayment Model."""

    def setUp(self):
        password = "testpass123"

        self.borrower_user = user_create(
            email="borrower@example.com",
            password=password,
            group_name="borrower",
        )
        self.borrower_target_100_repaid_50 = loan_profile_create(
            user=self.borrower_user,
            profile_img="https://www.example.com/photo.jpg",
            title="loan profile 1",
            description="loan profile 1",
            loan_duration=12,
            target_amount=100,
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )

        self.lender_a = user_create(
            email="lenderA@example.com",
            password=password,
            group_name="lender",
            amount_available=50,
        )

        self.lender_b = user_create(
            email="lenderB@example.com",
            password=password,
            group_name="lender",
            amount_available=50,
        )

        self.contribution_a = contribution_create(
            lender=self.lender_a,
            borrower=self.borrower_target_100_repaid_50,
            amount=50,
        )

        self.contribution_b = contribution_create(
            lender=self.lender_b,
            borrower=self.borrower_target_100_repaid_50,
            amount=50,
        )

    def test_borrower_can_make_single_repayment(self):
        """
        Test that a lender can contribute to loan_profile
        """
        repayment_amount = Money(50, "USD")
        repayment = repayment_create(
            borrower=self.borrower_target_100_repaid_50,
            amount=repayment_amount,
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
        repayment_a = repayment_create(
            borrower=self.borrower_target_100_repaid_50,
            amount=repayment_amount_a,
        )
        repayment_b = repayment_create(
            borrower=self.borrower_target_100_repaid_50,
            amount=repayment_amount_b,
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
