"""Database models."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models, transaction
from djmoney.models.fields import MoneyField
from djmoney.money import Money


from model_utils.models import TimeStampedModel

from .helpers import make_repayment
from .utils import one_year_from_now_date
from .operations import app_to_borrower, borrower_to_app

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @classmethod
    def create_category(cls, name):
        """Creates and returns a new category instance."""
        category, created = cls.objects.get_or_create(name=name)
        return category


class LoanProfileStatus(models.IntegerChoices):
    """Loan profile statuses."""

    PENDING = 1, "Pending"
    APPROVED = 2, "Approved"
    REJECTED = 3, "Rejected"


class LoanProfile(TimeStampedModel):
    """Loan profile model."""

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

    @classmethod
    def create_loan_profile(
        cls,
        user,
        title,
        target_amount,
        description="",
        story="",
        loan_duration=12,
        deadline_to_receive_loan=None,
        category_names=None,
        **extra_fields,
    ):
        """Create a new LoanProfile instance and assigns categories."""

        if not isinstance(target_amount, Money):
            target_amount = Money(
                target_amount, settings.DEFAULT_MONEY_CURRENCY
            )

        loan_profile = cls.objects.create(
            user=user,
            title=title,
            target_amount=target_amount,
            description=description,
            story=story,
            loan_duration=loan_duration,
            deadline_to_receive_loan=deadline_to_receive_loan
            or one_year_from_now_date(),
            **extra_fields,
        )

        # Add categories (creating if necessary)
        if category_names:
            for name in category_names:
                category = Category.create_category(name)
                loan_profile.categories.add(category)

        return loan_profile

    def __str__(self):
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

    def get_payment(self):
        """REAL-MONEY: Get payment from app."""
        self.is_paid_raised_amount = True
        self.save()

        return app_to_borrower(self, self.total_raised())

    def make_payment(self):
        """REAL-MONEY: Make payment to app."""
        self.has_repaid = True
        self.save()

        return borrower_to_app(
            self, self.total_repaid(), self.remaining_balance()
        )

    def make_repayment(self, amount):
        """Make repayment."""
        return make_repayment(self, amount)

    def apply_repayments(self):
        """Apply all repayments to contributors proportionally."""
        repayments = self.repayments.all()
        return list(map(lambda r: r.repay_lenders(), repayments))


class Contribution(TimeStampedModel):
    """Represents a financial contribution from a lender to a borrower."""

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

    def __str__(self):
        return f"{self.lender} contributed {self.amount} to {self.borrower}"

    class Meta:
        ordering = ["-created"]


class Repayment(TimeStampedModel):
    """
    Represents a repayment made by a borrower.

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

    def repay_lenders(self):
        """Repay lenders from this amount."""

        def repay_lender(contribution):
            def cut():
                return Money(
                    self.amount.amount
                    * contribution.amount.amount
                    / self.borrower.total_raised().amount,
                    "USD",
                )

            contribution.lender.amount_available += cut()
            contribution.lender.save()

        if not self.is_applied:
            with transaction.atomic():
                for contribution in self.borrower.contributions.all():
                    repay_lender(contribution)

                self.is_applied = True
                self.save()

    def __str__(self):
        return f"{self.borrower} repaid {self.amount} on {self.created}"

    class Meta:
        ordering = ["-created"]
