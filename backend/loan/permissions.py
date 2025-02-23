from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow only the owner of a LoanProfile to edit or delete it."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the LoanProfile
        return obj.user == request.user
