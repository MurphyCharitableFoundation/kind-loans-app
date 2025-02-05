from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from loan.operations import app_to_lender, lender_to_app
from model_utils.models import TimeStampedModel
from phonenumber_field.modelfields import PhoneNumberField

from .managers import UserManager


class User(AbstractUser, TimeStampedModel):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    profile_img = models.ImageField(
        upload_to="user_images/",
        blank=True,
        null=True,
        help_text="Profile image url for the user.",
    )
    amount_available = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, "USD"),
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def purchase_credits(self, amount):
        """REAL-MONEY: Purchase credits from application."""

        self.amount_available += amount
        self.save()

        return lender_to_app(self, amount)

    def withdraw_credits(self, amount):
        """REAL-MONEY: Withdraw credits from application."""

        if amount > self.amount_available:
            ValueError("User may not withdraw more than have available.")

        self.amount_available -= amount
        self.save()

        return app_to_lender(self, amount)

    def __str__(self):
        return f"User: {self.email}"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]
