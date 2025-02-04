from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from core import models
from core import helpers

from djmoney.money import Money
from faker import Faker
from datetime import timedelta


class Command(BaseCommand):
    help = "Generate fake data for User, LoanProfile, and Transaction Model."

    def add_arguments(self, parser):
        parser.add_argument(
            "lender_count", type=int, help="The number of lenders"
        )
        parser.add_argument(
            "borrower_count",
            type=int,
            help="The number of borrowers with loan profiles",
        )

    def handle(self, *args, **kwargs):
        fake = Faker()

        LENDER_COUNT = kwargs["lender_count"]
        BORROWER_COUNT = kwargs["borrower_count"]
        LOAN_PERIOD = timedelta(days=500)

        def get_amount(n=3):
            return fake.pydecimal(left_digits=3, right_digits=2, positive=True)

        def create_n_lenders(n):
            for _ in range(LENDER_COUNT):
                name = fake.name()
                first, last = list(map(str.lower, name.split()))[:2]

                lender = get_user_model().objects.create_user(
                    first_name=first,
                    last_name=last,
                    email=f"{first}.{last}@example.com",
                    password=fake.name(),
                    role=models.UserRole.LENDER,
                )
                helpers.make_payment(lender, Money(100, "USD"))

        def create_n_borrowers(n):
            # fake-borrowers & loan-profiles
            for _ in range(BORROWER_COUNT):
                name = fake.name()
                first, last = list(map(str.lower, name.split()))[:2]

                user = get_user_model().objects.create_user(
                    first_name=first,
                    last_name=last,
                    email=f"{first}.{last}@example.com",
                    password=fake.name(),
                )
                models.LoanProfile.objects.create(
                    user=user,
                    photoURL=fake.image_url(width=640, height=480),
                    title=fake.company(),
                    description=fake.paragraph(nb_sentences=4),
                    categories="agribusiness",
                    loan_duration_months=fake.random_number(digits=2),
                    total_amount_required=Money(50, "USD"),
                    deadline_to_receive_loan=fake.date_between(
                        start_date="today", end_date=LOAN_PERIOD
                    ),
                )

        def create_transactions():
            random_lenders = models.User.objects.filter(
                role=models.UserRole.LENDER
            ).order_by("?")[:LENDER_COUNT]
            random_loan_profiles = models.LoanProfile.objects.order_by("?")[
                :BORROWER_COUNT
            ]

            for lender in random_lenders:
                for loan_profile in random_loan_profiles:
                    for n in range(fake.random_number(digits=1)):
                        helpers.make_contribution(
                            lender, loan_profile, Money(get_amount(2), "USD")
                        )

                    loan_profile.get_payment()
                    helpers.make_repayment(
                        loan_profile, loan_profile.total_raised()
                    )
                    loan_profile.make_payment()

        create_n_lenders(LENDER_COUNT)
        self.stdout.write(
            self.style.SUCCESS(f"{LENDER_COUNT} lender(s) created.")
        )

        create_n_borrowers(BORROWER_COUNT)
        self.stdout.write(
            self.style.SUCCESS(
                f"{BORROWER_COUNT} borrower(s) with loan profiles created."
            )
        )

        # create_transactions()
        # self.stdout.write(self.style.SUCCESS("Created sample transactions"))

        self.stdout.write(self.style.SUCCESS("DONE: Generated Samples."))
