"""Helpers for Loan app."""


def make_payment(lender, amount, **kwargs):
    """Create a payment for in-app credits."""
    return lender.purchase_credits(amount)


def make_payout(lender, amount, **kwargs):
    """Create a payout from in-app credits."""
    return lender.withdraw_credits(amount)
