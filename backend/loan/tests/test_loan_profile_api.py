from django.contrib.auth import get_user_model
from djmoney.money import Money
from loan.models import LoanProfile
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from ..services import category_create

User = get_user_model()


class LoanProfileAPITestCase(APITestCase):
    """Tests for the LoanProfile API."""

    def setUp(self):
        """Setup test data."""
        self.client = APIClient()

        # Create users (email-based authentication)
        self.user = User.objects.create_user(
            email="user1@example.com", password="testpass"
        )
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )

        # Create categories
        self.category = category_create(name="Education")

        # Create a LoanProfile
        self.loan_profile = LoanProfile.objects.create(
            user=self.user,
            title="Education Loan",
            description="Help students with tuition",
            story="I need support for my studies",
            target_amount=Money(1000.00, "USD"),
        )
        self.loan_profile.categories.add(self.category)

        self.url = f"/api/loan/profile/{self.loan_profile.id}/"

    def test_get_loan_profile_list(self):
        """Test retrieving a list of loan profiles."""
        response = self.client.get("/api/loan/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_get_loan_profile_detail(self):
        """Test retrieving a single loan profile."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Education Loan")

    def test_create_loan_profile(self):
        """Test creating a new loan profile."""
        self.client.force_authenticate(user=self.user)

        data = {
            "title": "New Loan",
            "description": "This is a new loan",
            "story": "A compelling story",
            "target_amount": "500.00",
            "categories": [self.category.name],
        }

        response = self.client.post("/api/loan/profile/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Loan")

    def test_create_loan_profile_unauthenticated(self):
        """Test creating a loan profile without authentication."""
        data = {
            "title": "Loan Without Auth",
            "target_amount": "1000.00",
        }
        response = self.client.post("/api/loan/profile/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_loan_profile(self):
        """Test updating an existing loan profile."""
        self.client.force_authenticate(user=self.user)

        data = {"title": "Updated Loan"}
        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Loan")

    def test_update_loan_profile_unauthorized(self):
        """Test that another user cannot update someone else's loan profile."""
        other_user = User.objects.create_user(
            email="user2@example.com", password="testpass"
        )
        self.client.force_authenticate(user=other_user)

        data = {"title": "Unauthorized Update"}
        response = self.client.patch(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_loan_profile(self):
        """Test deleting a loan profile."""
        self.client.force_authenticate(user=self.user)

        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            LoanProfile.objects.filter(id=self.loan_profile.id).exists()
        )

    def test_get_loan_profile_story(self):
        """Test accessing the story endpoint."""
        response = self.client.get(f"{self.url}story/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["story"], "I need support for my studies"
        )

    def test_get_loan_profile_story_not_found(self):
        """Test accessing story for a non-existing loan profile."""
        response = self.client.get("/api/loan/profile/999/story/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
