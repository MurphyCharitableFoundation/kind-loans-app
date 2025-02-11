from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Ensures the required user groups exist in the database."

    def handle(self, *args, **options):
        group_names = ["admin", "lender", "borrower"]
        created_groups = []

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                created_groups.append(group_name)

        if created_groups:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Created groups: {', '.join(created_groups)}"
                )
            )
        else:
            self.stdout.write(self.style.SUCCESS("All groups already exist."))
