"""Core Utils."""

from django.utils import timezone


def one_year_from_now():
    """Return a date one year from now."""
    return timezone.now() + timezone.timedelta(days=365)
