"""User services."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def user_create(email: str, password: str, group_name: str, **kwargs) -> User:
    """
    Create a user given email and password, assigns them to a group.

    - The group name is **case-insensitive** and is always stored in lowercase.
    - If the group does not exist,
      it will be created **only if it's in the allowed list**.
    - If the group is not in the allowed list, it will be ignored.

    Allowed groups: ["admin", "lender", "borrower"]
    """
    allowed_groups = {"admin", "lender", "borrower"}

    # Normalize group name (case-insensitive, lowercase)
    normalized_group_name = group_name.lower()

    user = User.objects.create_user(email=email, password=password, **kwargs)

    if normalized_group_name in allowed_groups:
        group, _ = Group.objects.get_or_create(name=normalized_group_name)
        user.groups.add(group)

    return user
