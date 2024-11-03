"""
Database models.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from cities_light.models import Country, City

from decimal import Decimal


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
    first_name = models.CharField(
        max_length=255, help_text="The first name of the user."
    )
    last_name = models.CharField(
        max_length=255, help_text="The last name of the user."
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
    interests = models.JSONField(
        blank=True, default=list, help_text="The interests of the user."
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

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["email"]

    def __str__(self):
        return self.email


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
    total_amount_required = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The total amount required for the loan.",
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

    @property
    def amount_lended_to_date(self):
        transaction_total = self.transactions.filter(
            status=TransactionStatus.COMPLETED
        ).aggregate(models.Sum("amount"))["amount__sum"]

        return (
            transaction_total.quantize(Decimal("0.00"))
            if transaction_total
            else 0
        )

    class Meta:
        verbose_name = "Loan Profile"
        verbose_name_plural = "Loan Profiles"
        ordering = ["user"]

    def __str__(self):
        return f"{self.user.name}'s loan profile"


class TransactionManager(models.Manager):
    """Manager for transactions."""

    def create_transaction(self, lender, borrower, amount, **extra_fields):
        """Create, save, and return a new transaction."""
        # user must be User that is lender
        if lender.role != UserRole.LENDER:
            raise ValueError("Transaction must be initiated by lender.")
        # TODO:
        # borrower must be a loan-profile
        # must be before the loan-profile cutoff
        transaction = self.model(
            user=lender, loan_profile=borrower, amount=amount, **extra_fields
        )
        transaction.save(using=self._db)

        return transaction


class TransactionStatus(models.IntegerChoices):
    """Transaction Status choices."""

    PENDING = 1, "Pending"  # Payment initiated but not yet processed
    COMPLETED = 2, "Completed"  # Payment successfully completed
    FAILED = 3, "Failed"  # Payment attempt failed
    REFUNDED = 4, "Refunded"  # Payment was refunded
    CANCELED = 5, "Canceled"  # Payment was canceled by the user or system
    ON_HOLD = 6, "On Hold"  # Payment is temporarily on hold
    CHARGEBACK = 7, "Chargeback"  # Disputed payment


class PaymentMethod(models.IntegerChoices):
    """Payment Method choices."""

    CREDIT_CARD = 1, "Credit Card"
    DEBIT_CARD = 2, "Debit Card"
    PAYPAL = 3, "PayPal"
    APPLE_PAY = 4, "Apple Pay"
    GOOGLE_PAY = 5, "Google Pay"
    BANK_TRANSFER = 6, "Bank Transfer"
    CASH = 7, "Cash"
    CRYPTOCURRENCY = 9, "Cryptocurrency"


# TODO:
# + currency
# + on-delete: transactions cannot be deleted for audit reasons
#   instead prevent delete on user object or loanprofile, resort to
#   hiding/making inactive
class Transaction(models.Model):
    """Transaction model."""

    loan_profile = models.ForeignKey(
        LoanProfile,
        related_name="transactions",
        on_delete=models.PROTECT,
        help_text="The borrower (loan profile) for the transaction.",
    )
    user = models.ForeignKey(
        User,
        related_name="transactions",
        on_delete=models.PROTECT,
        help_text="The lender for the transaction.",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="The amount for the transaction.",
    )
    transaction_date = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the transaction occurred.",
    )
    payment_method = models.IntegerField(
        choices=PaymentMethod.choices,
        default=PaymentMethod.PAYPAL,
        help_text="The method of payment for the transaction.",
    )
    status = models.IntegerField(
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
        help_text="The status of the transaction.",
    )

    objects = TransactionManager()

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-transaction_date"]

    def __str__(self):
        return f"{self.user.name} ----({self.amount})----> {self.loan_profile}"

    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Transaction amount cannot be negative.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Transaction cannot be deleted.")

    def delete_queryset(self, qs, *args, **kwargs):
        raise ValidationError("Bulk deletion is not allowed for Transactions.")
