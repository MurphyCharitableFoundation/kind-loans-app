"""Money operations between app, lender, and borrower."""

from accounting.utils import config_platform_accounts


def lender_to_app(lender, amount):
    """Track amount from lender to app."""
    accounts = config_platform_accounts()

    return accounts["payables"].transfer_to(
        to_account=accounts["cash"],
        amount=amount,
        description=f"User {lender} added funds to their account",
    )


def app_to_borrower(borrower, amount):
    """Track amount from app to borrower."""
    accounts = config_platform_accounts()

    return accounts["cash"].transfer_to(
        to_account=accounts["receivables"],
        amount=amount,
        description=f"Disbursed funds to {borrower}",
    )


def borrower_to_app(borrower, amount, amount_outstanding):
    """
    Track amount from borrower to app.

    Also track any amount_outstanding as a write-off.
    """
    accounts = config_platform_accounts()

    if amount_outstanding:
        accounts["receivables"].transfer_to(
            to_account=accounts["bad_debt"],
            amount=amount_outstanding,
            description=f"Written off as bad debt; non-payment by {borrower}",
        )

    return accounts["receivables"].transfer_to(
        to_account=accounts["cash"],
        amount=amount,
        description=f"Borrower {borrower} repaid app",
    )


def app_to_lender(lender, amount):
    """Track amount from app to lender."""
    accounts = config_platform_accounts()

    return accounts["cash"].transfer_to(
        to_account=accounts["payables"],
        amount=-amount,
        description=f"Payout to lender: {lender}",
    )
