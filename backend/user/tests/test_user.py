from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()  # ✅ Ensures compatibility with custom User model


class UserManagerTests(TestCase):

    def test_create_user_without_username(self):
        """Test that a user can be created with just an email and password."""
        user = User.objects.create_user(
            email="testuser@example.com", password="securepass123"
        )

        self.assertTrue(
            User.objects.filter(email="testuser@example.com").exists()
        )
        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password("securepass123"))

    def test_create_user_without_email_raises_error(self):
        """Test that trying to create a user without an email raises
        an error."""
        with self.assertRaises(ValueError) as error:
            User.objects.create_user(email="", password="securepass123")

        self.assertEqual(str(error.exception), "The Email must be set")

    def test_create_superuser(self):
        """Test that a superuser is created correctly."""
        admin_user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass456"
        )

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_without_staff_flag_raises_error(self):
        """Test that creating a superuser without is_staff=True raises
        an error."""
        with self.assertRaises(ValueError) as error:
            User.objects.create_superuser(
                email="superuser@example.com",
                password="superpass789",
                is_staff=False,
            )

        self.assertEqual(
            str(error.exception), "Superuser must have is_staff=True."
        )

    def test_create_superuser_without_superuser_flag_raises_error(self):
        """Test that creating a superuser without is_superuser=True
        raises an error."""
        with self.assertRaises(ValueError) as error:
            User.objects.create_superuser(
                email="superuser@example.com",
                password="superpass789",
                is_superuser=False,
            )

        self.assertEqual(
            str(error.exception), "Superuser must have is_superuser=True."
        )
