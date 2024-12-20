"""
Database models.
"""

from django.db import models, transaction
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from model_utils.models import TimeStampedModel
from cities_light.models import Country, City
from djmoney.money import Money
from djmoney.models.fields import MoneyField

from .operations import (
    lender_to_app,
    app_to_lender,
    app_to_borrower,
    borrower_to_app,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save, and return a new user."""
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create, save, and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.role = "admin"
        user.save(using=self._db)

        return user


class UserRole(models.TextChoices):
    """User roles."""

    LENDER = "lender", "Lender"
    BORROWER = "borrower", "Borrower"
    ADMIN = "admin", "Admin"


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(
        max_length=255, unique=True, help_text="The email address of the user."
    )
    name = models.CharField(
        max_length=255, help_text="The full name of the user."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.BORROWER,
        help_text="The role of the user in the system.",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The country where the user is located.",
    )
    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="The city where the user is located.",
    )
    business_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="The name of the user's business, if applicable.",
    )
    business_type = models.CharField(
        max_length=255, blank=True, help_text="The user's business type."
    )
    interests = models.TextField(
        blank=True, help_text="The interests of the user."
    )
    photoURL = models.URLField(
        blank=True, help_text="The URL of the user's photo."
    )
    story = models.TextField(
        blank=True, help_text="The personal story of the user."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the user was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the user was last updated.",
    )
    amount_available = MoneyField(
        max_digits=10,
        decimal_places=2,
        default=Money(0, "USD"),
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    def purchase_credits(self, amount):
        """
        REAL-MONEY: Purchase credits from application
        """
        self.amount_available += amount
        self.save()

        return lender_to_app(self, amount)

    def withdraw_credits(self, amount):
        """
        REAL-MONEY: Withdraw credits from application
        """
        if amount > self.amount_available:
            ValueError("User may not withdraw more than have available.")

        self.amount_available -= amount
        self.save()

        return app_to_lender(self, amount)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]


class LoanProfileStatus(models.IntegerChoices):
    """Loan profile statuses."""

    PENDING = 1, "Pending"
    APPROVED = 2, "Approved"
    REJECTED = 3, "Rejected"


class LoanProfile(models.Model):
    """Loan profile model."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="loan_profiles",
        help_text="The user associated with the loan profile.",
    )
    photoURL = models.URLField(
        help_text="The URL of the photo for the loan profile."
    )
    title = models.CharField(
        max_length=255, help_text="The title of the loan profile."
    )
    description = models.TextField(
        help_text="The description of the loan profile."
    )
    business_type = models.CharField(
        max_length=255, help_text="The type of business for the loan profile."
    )
    loan_duration_months = models.IntegerField(
        help_text="The duration of the loan in months.", default=12
    )
    total_amount_required = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )
    is_paid_raised_amount = models.BooleanField(
        default=False, help_text="Has been paid raised amount."
    )
    has_repaid = models.BooleanField(
        default=False,
        help_text="Has repaid (some or all) of raised amount by deadline.",
    )
    deadline_to_receive_loan = models.DateField(
        help_text="The deadline to receive the loan.",
        default=timezone.now() + timezone.timedelta(days=365),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the loan profile was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the loan profile was last updated.",
    )
    status = models.IntegerField(
        choices=LoanProfileStatus.choices,
        default=LoanProfileStatus.PENDING,
        help_text="The status of the loan profile.",
    )

    class Meta:
        verbose_name = "Loan Profile"
        verbose_name_plural = "Loan Profiles"
        ordering = ["user"]

    def __str__(self):
        return f"{self.user.name}'s {self.title}"

    # TODO: Give this from ops:app_to_borrower
    def total_raised(self):
        """
        Calculate the total amount raised for this borrower.
        """
        total = (
            self.contributions.aggregate(total=models.Sum("amount"))["total"]
            or 0
        )

        return Money(total, "USD")

    # TODO: To compute (total) amount for ops:borrower_to_app
    def total_repaid(self):
        """
        Calculate the total amount repaid by this borrower.
        """
        total = (
            self.repayments.aggregate(total=models.Sum("amount"))["total"] or 0
        )

        return Money(total, "USD")

    # TODO: To compute bad-debt for ops:borrower_to_app
    def remaining_balance(self):
        """
        Calculate the remaining balance to be repaid.
        """
        return self.total_raised() - self.total_repaid()

    def has_applied_all_repayments(self):
        return all(r.is_applied for r in self.repayments.all())

    def get_payment(self):
        """
        REAL-MONEY: Get payment from app.
        """
        self.is_paid_raised_amount = True
        self.save()

        return app_to_borrower(self, self.total_raised())

    def make_payment(self):
        """
        REAL-MONEY: Make payment to app.
        """
        self.has_repaid = True
        self.save()

        return borrower_to_app(
            self, self.total_repaid(), self.remaining_balance()
        )

    def apply_repayments(self):
        """
        Apply all repayments to contributors proportionally
        """
        repayments = self.repayments.all()
        return list(map(lambda r: r.repay_lenders(), repayments))


class Contribution(TimeStampedModel):
    """
    Represents a financial contribution from a lender to a borrower.
    """

    lender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contributions"
    )
    loan_profile = models.ForeignKey(
        LoanProfile, on_delete=models.CASCADE, related_name="contributions"
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )

    def __str__(self):
        return (
            f"{self.lender} contributed {self.amount} to {self.loan_profile}"
        )

    class Meta:
        ordering = ["-created"]


class Repayment(TimeStampedModel):
    """
    Represents a repayment made by a borrower.
    Each borrower can make multiple repayments.
    """

    loan_profile = models.ForeignKey(
        LoanProfile, on_delete=models.CASCADE, related_name="repayments"
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )
    description = models.TextField(
        blank=True, null=True, help_text="Optional notes about the repayment"
    )
    is_applied = models.BooleanField(
        default=False,
    )

    def repay_lenders(self):
        """
        Repay lenders from this amount.
        """

        def repay_lender(contribution):
            def cut():
                return Money(
                    self.amount.amount
                    * contribution.amount.amount
                    / self.loan_profile.total_raised().amount,
                    "USD",
                )

            contribution.lender.amount_available += cut()
            contribution.lender.save()

        if not self.is_applied:
            with transaction.atomic():
                for contribution in self.loan_profile.contributions.all():
                    repay_lender(contribution)

                self.is_applied = True
                self.save()

    def __str__(self):
        return f"{self.loan_profile} repaid {self.amount} on {self.created}"

    class Meta:
        ordering = ["-created"]
