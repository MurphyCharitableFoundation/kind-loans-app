"""
Tests for model interactions.
"""

from core.services import to_money
from django.contrib.auth import get_user_model
from django.test import TestCase

from ..services import (contribution_create, loan_profile_create,
                        repayment_apply, repayment_create, user_create)

User = get_user_model()


class ContributionAndRepaymentTests(TestCase):
    def setUp(self):
        password = "testpass123"

        self.b_user_a = user_create(
            email="borrower@example.com",
            password=password,
            group_name="borrower",
        )
        self.borrower_target_100 = loan_profile_create(
            user=self.b_user_a,
            title="Paid in Full",
            profile_img="https://www.example.com/photo.jpg",
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
            borrower=self.borrower_target_100,
            amount=50,
        )
        self.contribution_b = contribution_create(
            lender=self.lender_b,
            borrower=self.borrower_target_100,
            amount=50,
        )

    def test_repay_full_contributions_from_single_repayment(self):
        repayment = repayment_create(
            borrower=self.borrower_target_100, amount=100
        )

        self.assertFalse(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(0))
        self.assertEqual(self.lender_b.amount_available, to_money(0))

        repayment_apply(repayment=repayment)

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 50
        self.assertTrue(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(50))
        self.assertEqual(self.lender_b.amount_available, to_money(50))

    def test_repay_full_contributions_from_multiple_repayment(self):
        repayment_amount_a = to_money(40)
        repayment = repayment_create(
            borrower=self.borrower_target_100, amount=repayment_amount_a
        )

        self.assertFalse(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(0))
        self.assertEqual(self.lender_b.amount_available, to_money(0))

        repayment_apply(repayment=repayment)

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 20
        self.assertTrue(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(20))
        self.assertEqual(self.lender_b.amount_available, to_money(20))

    def test_repay_partial_contributions_from_single_repayment(self):
        repayment_amount_a = to_money(50)
        repayment = repayment_create(
            borrower=self.borrower_target_100, amount=repayment_amount_a
        )
        self.assertFalse(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(0))
        self.assertEqual(self.lender_b.amount_available, to_money(0))

        repayment_apply(repayment=repayment)

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 25
        self.assertTrue(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(25))
        self.assertEqual(self.lender_b.amount_available, to_money(25))

    def test_repay_partial_contributions_from_multiple_repayment(self):
        repayment_amount_a = to_money(20)
        repayment = repayment_create(
            borrower=self.borrower_target_100, amount=repayment_amount_a
        )
        self.assertFalse(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(0))
        self.assertEqual(self.lender_b.amount_available, to_money(0))

        repayment_apply(repayment=repayment)

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 10
        self.assertEqual(repayment.is_applied, True)
        self.assertEqual(self.lender_a.amount_available, to_money(10))
        self.assertEqual(self.lender_b.amount_available, to_money(10))

        repayment_amount_b = to_money(30)
        repayment = repayment_create(
            borrower=self.borrower_target_100, amount=repayment_amount_b
        )

        repayment_apply(repayment=repayment)

        self.lender_a.refresh_from_db()
        self.lender_b.refresh_from_db()

        # + 15
        self.assertTrue(repayment.is_applied)
        self.assertEqual(self.lender_a.amount_available, to_money(25))
        self.assertEqual(self.lender_b.amount_available, to_money(25))
