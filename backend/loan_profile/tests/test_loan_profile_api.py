"""
Tests for loan profile API.
"""

from djmoney.money import Money
from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import LoanProfile, LoanProfileStatus

from loan_profile.serializers import (
    LoanProfileSerializer,
    LoanProfileDetailSerializer,
)


LOAN_PROFILES_URL = reverse("loan_profile:loanprofile-list")


def detail_url(loan_profile_id):
    """Return loan profile detail URL."""
    return reverse("loan_profile:loanprofile-detail", args=[loan_profile_id])


def create_loan_profile(user, **params):
    """
    Create and return a new loan profile.
    """
    defaults = {
        "photoURL": "www.example.com/photo.jpg",
        "title": "Test title",
        "description": "Test description",
        "business_type": "Food",
        "loan_duration_months": 12,
        "total_amount_required": Money(500.00, "USD"),
        "deadline_to_receive_loan": "2022-01-01",
        "status": LoanProfileStatus.PENDING,
    }
    defaults.update(params)

    loan_profile = LoanProfile.objects.create(user=user, **defaults)
    return loan_profile


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicLoanProfileApiTests(TestCase):
    """Test the unauthenticated loan profile API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email="user@example.com", password="pass123")

    def test_auth_not_required(self):
        """Test authentication is not required for list of loan profiles."""
        res = self.client.get(reverse("loan_profile:loanprofile-list"))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_auth_required_for_loan_profile_detail(self):
        """Test authentication is required for loan profile detail."""
        loan_profile = create_loan_profile(user=self.user)
        url = detail_url(loan_profile.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_loan_profiles(self):
        """Test retrieving a list of loan profiles."""
        create_loan_profile(user=self.user)
        create_loan_profile(user=self.user)

        res = self.client.get(LOAN_PROFILES_URL)

        loan_profiles = LoanProfile.objects.all().order_by("-id")
        serializer = LoanProfileSerializer(loan_profiles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class PrivateLoanProfileApiTests(TestCase):
    """Test the authenticated user loan profile API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="user@example.com",
            password="pass123",
        )
        self.client.force_authenticate(self.user)

    def test_get_loan_profile_detail(self):
        """Test retrieving a loan profile detail."""
        loan_profile = create_loan_profile(user=self.user)
        url = detail_url(loan_profile.id)
        res = self.client.get(url)

        serializer = LoanProfileDetailSerializer(loan_profile)
        self.assertEqual(res.data, serializer.data)

    def test_create_loan_profile(self):
        """Test creating a new loan profile."""
        payload = {
            "photoURL": "https://www.example.com/photo.jpg",
            "title": "Test title",
            "description": "Test description",
            "business_type": "Food",
            "loan_duration_months": 12,
            "total_amount_required": 500,
            "deadline_to_receive_loan": date.today(),
            "status": LoanProfileStatus.PENDING,
        }
        res = self.client.post(LOAN_PROFILES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        loan_profile = LoanProfile.objects.get(id=res.data["id"])

        self.assertEqual(loan_profile.user, self.user)
