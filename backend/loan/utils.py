"""Loan Utils."""

from datetime import date, datetime

from django.utils import timezone


def one_year_from_now() -> datetime:
    """Return a datetime one year from now."""
    return timezone.now() + timezone.timedelta(days=365)


def one_year_from_now_date() -> date:
    """Return a date one year from now."""
    return one_year_from_now().date()
