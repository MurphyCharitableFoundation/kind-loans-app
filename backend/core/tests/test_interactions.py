"""
Tests for model interactions.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models, helpers

from djmoney.money import Money


class ContributionAndRepaymentTests(TestCase):
    def setUp(self):
        password = "testpass123"

        self.b_user_a = get_user_model().objects.create_user(
            email="borrower@example.com", password=password
        )
        self.borrower_target_100 = models.LoanProfile.objects.create(
            user=self.b_user_a,
            title="Paid in Full",
            photoURL="www.example.com/photo.jpg",
            description="loan profile 1",
            categories="agribusiness",
            loan_duration_months=12,
            total_amount_required=Money(100, "USD"),
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
            self.lender_a,
            self.borrower_target_100,
            Money(50, "USD"),
        )
        self.contribution_b = helpers.make_contribution(
            self.lender_b,
            self.borrower_target_100,
            Money(50, "USD"),
        )

    def test_repay_full_contributions_from_single_repayment(self):
        repayment = helpers.make_repayment(
            self.borrower_target_100, Money(100, "USD")
        )

        self.assertEqual(self.lender_a.amount_available, Money(0, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(0, "USD"))

        repayment.repay_lenders()

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 50
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, Money(50, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(50, "USD"))

    def test_repay_full_contributions_from_multiple_repayment(self):
        repayment_amount_a = Money(40, "USD")
        repayment = helpers.make_repayment(
            self.borrower_target_100, repayment_amount_a
        )

        self.assertEqual(self.lender_a.amount_available, Money(0, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(0, "USD"))

        repayment.repay_lenders()

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 20
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, Money(20, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(20, "USD"))

    def test_repay_partial_contributions_from_single_repayment(self):
        repayment_amount_a = Money(50, "USD")
        repayment = helpers.make_repayment(
            self.borrower_target_100, repayment_amount_a
        )

        self.assertEqual(self.lender_a.amount_available, Money(0, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(0, "USD"))

        repayment.repay_lenders()

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 25
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, Money(25, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(25, "USD"))

    def test_repay_partial_contributions_from_multiple_repayment(self):
        repayment_amount_a = Money(20, "USD")
        repayment = helpers.make_repayment(
            self.borrower_target_100, repayment_amount_a
        )

        self.assertEqual(self.lender_a.amount_available, Money(0, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(0, "USD"))

        repayment.repay_lenders()

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 10
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, Money(10, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(10, "USD"))

        repayment_amount_b = Money(30, "USD")
        repayment = helpers.make_repayment(
            self.borrower_target_100, repayment_amount_b
        )

        repayment.repay_lenders()

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 15
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, Money(25, "USD"))
        self.assertEqual(self.lender_b.amount_available, Money(25, "USD"))
