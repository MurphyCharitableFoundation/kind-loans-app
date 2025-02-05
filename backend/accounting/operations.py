from hordak.models import Account


def config_platform_accounts():
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


def lender_to_app(lender, amount):
    accounts = config_platform_accounts()

    return accounts["payables"].transfer_to(
        to_account=accounts["cash"],
        amount=amount,
        description=f"User {lender} added funds to their account",
    )


def app_to_borrower(borrower, amount):
    accounts = config_platform_accounts()

    return accounts["cash"].transfer_to(
        to_account=accounts["receivables"],
        amount=amount,
        description=f"Disbursed funds to {borrower}",
    )


def borrower_to_app(borrower, amount, amount_outstanding):
    """
    Borrower repaid app total amount that they could.
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
    accounts = config_platform_accounts()

    return accounts["cash"].transfer_to(
        to_account=accounts["payables"],
        amount=-amount,
        description=f"Payout to lender: {lender}",
    )
