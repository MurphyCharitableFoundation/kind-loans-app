from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Payment, PaymentStatus


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "platform",
        "amount",
        "status",
        "gateway_payment_id",
        "created",
    )
    list_filter = (
        "platform",
        "status",
        "created",
    )
    search_fields = (
        "user__username",
        "user__email",
        "gateway_payment_id",
    )
    readonly_fields = ("created", "modified")
    ordering = ("-created",)

    fieldsets = (
        (_("User Info"), {"fields": ("user",)}),
        (
            _("Payment Details"),
            {
                "fields": (
                    "platform",
                    "gateway_payment_id",
                    "transaction",
                    "amount",
                    "status",
                )
            },
        ),
        (_("Timestamps"), {"fields": ("created", "modified")}),
    )

    actions = ["mark_as_completed", "mark_as_failed"]

    @admin.action(description="Mark selected payments as Completed")
    def mark_as_completed(self, request, queryset):
        queryset.update(status=PaymentStatus.COMPLETED)

    @admin.action(description="Mark selected payments as Failed")
    def mark_as_failed(self, request, queryset):
        queryset.update(status=PaymentStatus.FAILED)
