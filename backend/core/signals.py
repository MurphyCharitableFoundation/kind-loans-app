from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_groups(sender, **kwargs):
    """Ensure required groups exist after migrations are applied."""
    if sender.name == "core":  # Prevent running on all apps
        for group_name in ["admin", "lender", "borrower"]:
            Group.objects.get_or_create(name=group_name)
