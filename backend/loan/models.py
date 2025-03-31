"""Database models."""

from core.services import to_money
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField
from djmoney.money import Money
from model_utils.models import TimeStampedModel

from .utils import one_year_from_now_date

User = get_user_model()


class Category(models.Model):
    """Representation of Category."""

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """Represent Category as str."""
        return self.name


class LoanProfileStatus(models.IntegerChoices):
    """Loan profile statuses."""

    PENDING = 1, "Pending"
    APPROVED = 2, "Approved"
    REJECTED = 3, "Rejected"


class LoanProfile(TimeStampedModel):
    """Representation of Loan Profile."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="loan_profiles",
        help_text="The user associated with the loan profile.",
    )
    profile_img = models.URLField(
        help_text="The URL of the photo for the loan profile.",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=255,
        help_text="The title of the loan profile.",
        null=True,
        blank=True,
    )
    description = models.TextField(
        help_text="The description of the loan profile.", null=True, blank=True
    )
    story = models.TextField(
        help_text="A short description of the user and their reason why.",
        null=True,
        blank=True,
    )
    loan_duration = models.IntegerField(
        help_text="The duration of the loan in months.",
        default=12,
        null=True,
        blank=True,
    )
    target_amount = MoneyField(
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
        default=one_year_from_now_date,
    )
    status = models.IntegerField(
        choices=LoanProfileStatus.choices,
        default=LoanProfileStatus.PENDING,
        help_text="The status of the loan profile.",
    )
    categories = models.ManyToManyField(
        Category, related_name="loan_profiles", blank=True
    )
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Loan Profile"
        verbose_name_plural = "Loan Profiles"
        ordering = ["-created"]

    def __str__(self):
        """Represent Loan Profile as str."""
        return f"Loan Profile: {self.title} by {self.user.get_full_name()}"

    def total_raised(self):
        """Calculate the total amount raised for this borrower."""
        total = (
            self.contributions.aggregate(total=models.Sum("amount"))["total"]
            or 0
        )

        return Money(total, "USD")

    def total_repaid(self):
        """Calculate the total amount repaid by this borrower."""
        total = (
            self.repayments.aggregate(total=models.Sum("amount"))["total"] or 0
        )

        return Money(total, "USD")

    def remaining_balance(self):
        """Calculate the remaining balance to be repaid."""
        return self.total_raised() - self.total_repaid()

    def has_applied_all_repayments(self):
        """If all repayments are applied, then True."""
        return all(r.is_applied for r in self.repayments.all())


class Contribution(TimeStampedModel):
    """Represent a financial contribution from a lender to a borrower."""

    lender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="contributions",
        help_text="The lender (user) making this contribution.",
    )
    borrower = models.ForeignKey(
        LoanProfile,
        on_delete=models.CASCADE,
        related_name="contributions",
        help_text="The borrower (loan profile) that will be supported.",
    )
    amount = MoneyField(
        max_digits=10,
        decimal_places=2,
        default_currency="USD",
        validators=[MinValueValidator(Money(0.01, "USD"))],
    )

    def clean(self):
        """Validate Contribution before save."""
        max_contribution = self.lender.amount_available
        if self.amount > max_contribution:
            raise ValidationError(
                {"amount": f"Amount <= lender's funds: {max_contribution}."}
            )

        if self.amount <= to_money(0):
            raise ValidationError(
                {"amount": "Amount cannot be negative or zero."}
            )

        total_raised = self.borrower.total_raised()
        rfn = self.borrower.target_amount - total_raised
        if self.amount > rfn:
            raise ValidationError(
                {"amount": f"Amount <= remaining funding need {rfn}"}
            )

    def __str__(self):
        """Represent Contribution as str."""
        return "Contribution: {} contributed {} to {}".format(
            self.lender, self.amount, self.borrower
        )

    class Meta:
        ordering = ["-created"]


class Repayment(TimeStampedModel):
    """
    Represent a repayment made by a borrower.

    Each borrower can make multiple repayments.
    """

    borrower = models.ForeignKey(
        LoanProfile,
        on_delete=models.CASCADE,
        related_name="repayments",
        help_text="The borrower (loan profile) making this repayment.",
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
        help_text="True if the repayment has been paid out to contributors.",
    )

    def clean(self):
        """Validate Repayment before saving."""
        rb = self.borrower.remaining_balance()
        if self.amount > rb:
            raise ValidationError(
                {"amount": f"Amount <= loan profile remaining balance {rb}"}
            )

        if self.amount <= to_money(0):
            raise ValidationError(
                {"amount": "Amount cannot be negative or zero."}
            )

    def __str__(self):
        """Represent Repayment as str."""
        return "Repayment: {} repaid {} on {}".format(
            self.borrower, self.amount, self.created
        )

    class Meta:
        ordering = ["-created"]
