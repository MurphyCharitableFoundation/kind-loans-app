from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from djmoney.money import Money
from hordak.models import Leg, StatementImport, Transaction
from loan.models import Contribution, Repayment

User = get_user_model()


class Command(BaseCommand):
    help = "Reset all Accounts, delete all Transactions."

    def handle(self, *args, **kwargs):
        # Delete Legs (debits/credits within transactions)
        Leg.objects.all().delete()

        Transaction.objects.all().delete()

        StatementImport.objects.all().delete()

        # Account.objects.all().delete()

        Contribution.objects.all().delete()

        Repayment.objects.all().delete()

        User.objects.update(amount_available=Money(0, "USD"))

        self.stdout.write(
            self.style.SUCCESS(
                "DONE: Reset all Accounts, Contributions, and Repayments."
            )
        )
