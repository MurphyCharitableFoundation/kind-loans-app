"""Command: Generate Sample Data."""

from datetime import timedelta
from core.utils import assign_user_group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from djmoney.money import Money
from faker import Faker
from loan import models, services

User = get_user_model()


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

        def ensure_groups():
            for group_name in ["admin", "lender", "borrower"]:
                Group.objects.get_or_create(name=group_name)

        def get_amount(n=3):
            return fake.pydecimal(left_digits=3, right_digits=2, positive=True)

        def get_all_lenders():
            return Group.objects.get(name="lender").user_set.all()

        def get_all_borrowers():
            return Group.objects.get(name="borrower").user_set.all()

        def create_n_lenders(n):
            for _ in range(LENDER_COUNT):
                name = fake.name()
                first, last = list(map(str.lower, name.split()))[:2]

                lender = User.objects.create_user(
                    first_name=first,
                    last_name=last,
                    email=f"{first}.{last}@example.com",
                    password=fake.name(),
                )
                assign_user_group(lender, "lender")

                services.lender_make_payment(lender, 100)

        def create_n_borrowers(n):
            # fake-borrowers & loan-profiles
            for _ in range(BORROWER_COUNT):
                name = fake.name()
                first, last = list(map(str.lower, name.split()))[:2]

                borrower = User.objects.create_user(
                    first_name=first,
                    last_name=last,
                    email=f"{first}.{last}@example.com",
                    password=fake.name(),
                )
                assign_user_group(borrower, "borrower")
                models.LoanProfile.objects.create(
                    user=borrower,
                    profile_img=fake.image_url(width=640, height=480),
                    title=fake.company(),
                    description=fake.paragraph(nb_sentences=4),
                    loan_duration=fake.random_number(digits=2),
                    target_amount=Money(50, "USD"),
                    deadline_to_receive_loan=fake.date_between(
                        start_date="today", end_date=LOAN_PERIOD
                    ),
                )

        def create_transactions():
            random_lenders = get_all_lenders()[:LENDER_COUNT]
            random_loan_profiles = models.LoanProfile.objects.order_by("?")[
                :BORROWER_COUNT
            ]

            for lender in random_lenders:
                for loan_profile in random_loan_profiles:
                    for n in range(fake.random_number(digits=1)):
                        services.contribution_create(
                            lender=lender,
                            borrower=loan_profile,
                            amount=Money(get_amount(2), "USD"),
                        )

                    loan_profile.get_payment()
                    services.repayment_create(
                        borrower=loan_profile,
                        amount=loan_profile.total_raised(),
                    )
                    loan_profile.make_payment()

        ensure_groups()
        self.stdout.write(
            self.style.SUCCESS("Admin, Lender, and Borrower groups created.")
        )

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
