from hordak.models import Account


PLATFORM_CASH_ACCOUNT, _ = Account.objects.get_or_create(
    name="platform_cash_account"
)
PLATFORM_BAD_DEBT, _ = Account.objects.get_or_create(name="platform_bad_debt")
PLATFORM_ACCOUNT_PAYABLES, _ = Account.objects.get_or_create(
    name="platform_account_payables"
)
PLATFORM_ACCOUNT_RECEIVABLES, _ = Account.objects.get_or_create(
    name="platform_account_receivables"
)


def lender_to_app(lender, amount):
    return PLATFORM_ACCOUNT_PAYABLES.transfer_to(
        to_account=PLATFORM_CASH_ACCOUNT,
        amount=amount,
        description=f"User {lender} added funds to their account",
    )


def app_to_borrower(borrower, amount):
    return PLATFORM_CASH_ACCOUNT.transfer_to(
        to_account=PLATFORM_ACCOUNT_RECEIVABLES,
        amount=amount,
        description=f"Disbursed funds to {borrower}",
    )


def borrower_to_app(borrower, amount, amount_outstanding):
    """
    Borrower repaid app total amount that they could.
    """
    if amount_outstanding:
        PLATFORM_ACCOUNT_RECEIVABLES.transfer_to(
            to_account=PLATFORM_BAD_DEBT,
            amount=amount_outstanding,
            description=f"Written off as bad debt; non-payment by {borrower}",
        )

    return PLATFORM_ACCOUNT_RECEIVABLES.transfer_to(
        to_account=PLATFORM_CASH_ACCOUNT,
        amount=amount,
        description=f"Borrower {borrower} repaid app",
    )


def app_to_lender(lender, amount):
    return PLATFORM_CASH_ACCOUNT.transfer_to(
        to_account=PLATFORM_ACCOUNT_PAYABLES,
        amount=-amount,
        description=f"Payout to lender: {lender}",
    )
