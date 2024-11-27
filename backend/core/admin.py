"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define then admin pages for users."""

    ordering = ["id"]
    list_display = ["email", "name", "role", "country", "city"]
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
                    "name",
                    "role",
                    "country",
                    "city",
                    "business_name",
                    "business_type",
                    "interests",
                    "photoURL",
                    "story",
                )
            },
        ),
    )
    readonly_fields = ["last_login"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "country",
                    "city",
                    "business_name",
                    "business_type",
                    "interests",
                    "photoURL",
                    "story",
                ),
            },
        ),
    )


class LoanProfileAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "total_amount_required",
        "amount_lended_to_date",
    )
    readonly_fields = ("amount_lended_to_date",)

    def amount_lended_to_date(self, obj):
        return obj.amount_lended_to_date


admin.site.register(models.User, UserAdmin)
admin.site.register(models.LoanProfile, LoanProfileAdmin)
