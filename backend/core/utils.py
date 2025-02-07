"""Core utilities."""

from django.contrib.auth.models import Group


def assign_user_group(user, group_name):
    """Assign user to a role-based group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
