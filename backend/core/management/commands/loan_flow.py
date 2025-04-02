"""Loan flow command."""

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Load test data for full repayment flow"

    def handle(self, *args, **kwargs):
        fixtures = [
            "users.json",
            "loan_profiles.json",
            "fund_lenders.json",
            "lenders_contribute.json",
            "pay_borrowers.json",
            "borrowers_repay.json",
            "apply_repayments.json",
            "lenders_withdraw.json",
        ]

        for fixture in fixtures:
            self.stdout.write(f"Loading {fixture}...")
            call_command("loaddata", fixture)
        self.stdout.write(self.style.SUCCESS("All fixtures loaded."))
