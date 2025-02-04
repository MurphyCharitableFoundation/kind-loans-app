from django.core.management.base import BaseCommand
from tagging.models import Tag


class Command(BaseCommand):
    help = "Create tags for Loan Profiles"

    def handle(self, *args, **options):
        tags = [
            "agribusiness",
            "arts & crafts",
            "beauty",
            "cleaning",
            "education",
            "environmental",
            "events & entertainment",
            "fashion",
            "health",
            "hospitality",
            "housing",
            "manufacturing",
            "retail & distribution",
            "tech & communications",
            "transportation",
            "watery & sanitation",
        ]
        created_tags = []

        for tag_name in tags:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            if created:
                created_tags.append(tag_name)

        if created_tags:
            self.stdout.write(
                self.style.SUCCESS(f"Created tags: {', '.join(created_tags)}")
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "No new tags were created. All tags already exist."
                )
            )
