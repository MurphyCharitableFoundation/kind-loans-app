from django.core.management.base import BaseCommand

from hordak.models import Transaction, StatementImport, Leg
from core.models import Contribution, Repayment, User

from djmoney.money import Money


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
