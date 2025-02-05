"""Utilities for double entry accounting."""

from hordak.models import Account


def config_platform_accounts():
    """Configure platform accounts."""
    PLATFORM_CASH_ACCOUNT, _ = Account.objects.get_or_create(
        name="platform_cash_account", type="AS", currencies=["USD"]
    )
    PLATFORM_BAD_DEBT, _ = Account.objects.get_or_create(
        name="platform_bad_debt", type="EX", currencies=["USD"]
    )
    PLATFORM_ACCOUNT_PAYABLES, _ = Account.objects.get_or_create(
        name="platform_account_payables", type="LI", currencies=["USD"]
    )
    PLATFORM_ACCOUNT_RECEIVABLES, _ = Account.objects.get_or_create(
        name="platform_account_receivables", type="AS", currencies=["USD"]
    )

    return {
        "bad_debt": PLATFORM_BAD_DEBT,
        "cash": PLATFORM_CASH_ACCOUNT,
        "payables": PLATFORM_ACCOUNT_PAYABLES,
        "receivables": PLATFORM_ACCOUNT_RECEIVABLES,
    }
