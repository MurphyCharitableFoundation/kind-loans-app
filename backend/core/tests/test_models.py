"""Tests for models."""

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models, helpers

from djmoney.money import Money


class ModelTests(TestCase):
    """Test user model"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that the email is normalized for new users"""
        sample_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2Example.com", "Test2Example.com"],
        ]
        for email, normalized_email in sample_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, normalized_email)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "sample122")

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            "test@example.com", "testpass123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_loan_profile(self):
        """Test creating a new loan profile"""
        user = get_user_model().objects.create_user(
            "test@example.com", "testpass123"
        )
        loan_profile = models.LoanProfile.objects.create(
            user=user,
            photoURL="www.example.com/photo.jpg",
            title="Test title",
            description="Test description",
            categories="agribusiness",
            loan_duration_months=12,
            total_amount_required=Money("500.00", "USD"),
            deadline_to_receive_loan="2021-12-31",
            status=1,
        )
        self.assertEqual(
            str(loan_profile),
            f"{loan_profile.title} by {user.first_name} {user.last_name}",
        )


class ContributionModelTests(TestCase):
    """ """

    def setUp(self):
        password = "testpass123"

        self.borrower_user = get_user_model().objects.create_user(
            email="borrower@example.com", password=password
        )
        self.borrower_target_100 = models.LoanProfile.objects.create(
            user=self.borrower_user,
            photoURL="www.example.com/photo.jpg",
            description="loan profile 1",
            categories="agribusiness",
            loan_duration_months=12,
            total_amount_required=Money(100, "USD"),
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


class RepaymentModelTests(TestCase):
    """ """

    def setUp(self):
        password = "testpass123"

        self.borrower_user = get_user_model().objects.create_user(
            email="borrower@example.com", password=password
        )
        self.borrower_target_100_repaid_50 = models.LoanProfile.objects.create(
            user=self.borrower_user,
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
