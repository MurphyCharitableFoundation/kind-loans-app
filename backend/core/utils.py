"""Core utilities."""

from django.contrib.auth.models import Group
from django.http import Http404
from django.shortcuts import get_object_or_404


def get_object(model_or_queryset, **kwargs):
    """
    Get object by **kwargs from model_or_queryset.

    Reuse get_object_or_404 since the implementation
    supports both Model && queryset.

    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def assign_user_group(user, group_name):
    """Assign user to a role-based group."""
    group, _ = Group.objects.get_or_create(name=group_name)
    user.groups.add(group)
