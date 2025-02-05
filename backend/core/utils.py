"""Core utilities."""

from django.contrib.auth.models import Group


def assign_user_group(user, group_name):
    """Assign user to a role-based group."""
    group = Group.objects.get(name=group_name)
    user.groups.add(group)
