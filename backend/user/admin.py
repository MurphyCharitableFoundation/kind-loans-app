"""Django admin customization."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum
from django.utils.translation import gettext as _
from djmoney.money import Money

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    """Admin page(s) for User."""

    ordering = ["id"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "amount_available",
        "sum_of_contributions",
    ]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {"fields": ("is_active", "is_staff", "is_superuser")},
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "profile_img",
                )
            },
        ),
    )
    readonly_fields = ["last_login", "sum_of_contributions"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "profile_img",
                ),
            },
        ),
    )

    def sum_of_contributions(self, obj):
        """Sum of contributions for user."""
        total = obj.contributions.aggregate(total=Sum("amount"))["total"] or 0
        return Money(total, "USD")


admin.site.register(User, UserAdmin)
