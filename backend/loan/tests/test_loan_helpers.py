from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from loan.helpers import create_user_with_group

User = get_user_model()


class CreateUserWithGroupTests(TestCase):

    def test_create_user_with_valid_group_lowercase(self):
        """Test creating a user and assigning them to a valid group
        with lowercase input."""
        user = create_user_with_group(
            "testlender@example.com", "testpass123", "lender"
        )

        self.assertTrue(
            User.objects.filter(email="testlender@example.com").exists()
        )
        self.assertTrue(user.groups.filter(name="lender").exists())

    def test_create_user_with_valid_group_mixed_case(self):
        """Test creating a user with a valid group but using a
        mixed-case name."""
        user = create_user_with_group(
            "testborrower@example.com", "testpass123", "BoRrOwEr"
        )

        self.assertTrue(
            User.objects.filter(email="testborrower@example.com").exists()
        )
        self.assertTrue(user.groups.filter(name="borrower").exists())

    def test_create_user_with_invalid_group(self):
        """Test that an invalid group is ignored."""
        user = create_user_with_group(
            "testunknown@example.com", "testpass123", "Unknown"
        )

        self.assertTrue(
            User.objects.filter(email="testunknown@example.com").exists()
        )
        self.assertEqual(user.groups.count(), 0)  # ✅ No groups assigned

    def test_create_user_creates_group_if_missing(self):
        """Test that a missing valid group is created automatically
        and stored as lowercase."""
        self.assertFalse(Group.objects.filter(name="lender").exists())

        user = create_user_with_group(
            "testlender@example.com", "testpass123", "LENDER"
        )

        self.assertTrue(Group.objects.filter(name="lender").exists())
        self.assertTrue(user.groups.filter(name="lender").exists())
