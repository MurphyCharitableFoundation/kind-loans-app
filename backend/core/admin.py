"""Django admin customization."""

from django.contrib import admin, messages
from django.db.models import Sum
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from django.contrib.admin.options import (
    unquote,
    csrf_protect_m,
    HttpResponseRedirect,
)

from djmoney.money import Money
from tagging_autocomplete.widgets import TagAutocomplete
from tagging.forms import TagField
from tagging.models import Tag

from core import models


class UserAdmin(BaseUserAdmin):
    """Define then admin pages for users."""

    ordering = ["id"]
    list_display = [
        "email",
        "first_name",
        "last_name",
        "role",
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

    def sum_of_contributions(self, obj):
        total = obj.contributions.aggregate(total=Sum("amount"))["total"] or 0
        return Money(total, "USD")


class LoanProfileAdminForm(forms.ModelForm):
    """Loan Profile Admin with Autocompletion for Tagging."""

    categories = TagField(widget=TagAutocomplete())


class LoanProfileAdmin(admin.ModelAdmin):
    # form = LoanProfileAdminForm
    change_form_template = "admin/loan_profile_change_form.html"

    list_display = (
        "__str__",
        "total_amount_required",
        "sum_of_contributions",
        "sum_of_repayments",
        "get_tags",
    )
    readonly_fields = (
        "is_paid_raised_amount",
        "has_repaid",
        "sum_of_contributions",
        "sum_of_repayments",
    )

    def get_tags(self, obj):
        tags = Tag.objects.get_for_object(obj)
        return ", ".join(tag.name for tag in tags)

    get_tags.short_description = "Tags"

    actions = ["get_payment", "make_payment", "apply_repayments"]

    def get_payment(self, request, queryset):
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            obj.get_payment()
            updated_count = 1
        else:
            list(map(lambda lp: lp.get_payment(), queryset))
            updated_count = queryset.count()

        msg = "Paid {} borrower(s) from respective contributions.".format(
            updated_count
        )
        self.message_user(request, msg, messages.SUCCESS)

    def make_payment(self, request, queryset):
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            obj.make_payment()
            updated_count = 1
        else:
            list(map(lambda lp: lp.make_payment(), queryset))
            updated_count = queryset.count()

        msg = "Made loan repayment for {} borrower(s).".format(updated_count)
        self.message_user(request, msg, messages.SUCCESS)

    def apply_repayments(self, request, queryset):
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            obj.apply_repayments()
            updated_count = 1
        else:
            list(map(lambda r: r.apply_repayments(), queryset))
            updated_count = queryset.count()

        msg = "Applied repayments from {} loan profile(s).".format(
            updated_count
        )
        self.message_user(request, msg, messages.SUCCESS)

    get_payment.short_description = "Get Loan from Lender Contributions"
    make_payment.short_description = "Make Loan Repayment from Repayments"
    apply_repayments.short_description = "Apply repayments to Lenders"

    @csrf_protect_m
    def changeform_view(
        self, request, object_id=None, form_url="", extra_context=None
    ):
        if request.method == "POST":
            if "_get_payment" in request.POST:
                obj = self.get_object(request, unquote(object_id))
                self.get_payment(request, obj)
                return HttpResponseRedirect(request.get_full_path())

            if "_make_payment" in request.POST:
                obj = self.get_object(request, unquote(object_id))
                self.make_payment(request, obj)
                return HttpResponseRedirect(request.get_full_path())

            if "_apply_repayments" in request.POST:
                obj = self.get_object(request, unquote(object_id))
                self.apply_repayments(request, obj)
                return HttpResponseRedirect(request.get_full_path())

        return admin.ModelAdmin.changeform_view(
            self,
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def sum_of_contributions(self, obj):
        return obj.total_raised()

    def sum_of_repayments(self, obj):
        return obj.total_repaid()


class ContributionAdmin(admin.ModelAdmin):
    readonly_fields = ["lender", "loan_profile", "amount"]


class RepaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["loan_profile", "amount", "is_applied"]
    change_form_template = "admin/repayment_change_form.html"

    actions = ["apply_to_lenders"]

    def apply_to_lenders(self, request, queryset):
        if isinstance(queryset, models.Repayment):
            obj = queryset
            obj.repay_lenders()
            updated_count = 1
        else:
            queryset = queryset.filter(is_applied=False)
            list(map(lambda r: r.repay_lenders(), queryset))
            updated_count = queryset.count()

        msg = "Applied {} repayment to lenders by contribution amount".format(
            updated_count
        )
        self.message_user(request, msg, messages.SUCCESS)

    apply_to_lenders.short_description = "Apply repayment(s) to lenders"

    @csrf_protect_m
    def changeform_view(
        self, request, object_id=None, form_url="", extra_context=None
    ):
        if request.method == "POST" and "_apply_to_lenders" in request.POST:
            obj = self.get_object(request, unquote(object_id))
            self.apply_to_lenders(request, obj)
            return HttpResponseRedirect(request.get_full_path())

        return admin.ModelAdmin.changeform_view(
            self,
            request,
            object_id=object_id,
            form_url=form_url,
            extra_context=extra_context,
        )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.LoanProfile, LoanProfileAdmin)

admin.site.register(models.Contribution, ContributionAdmin)
admin.site.register(models.Repayment, RepaymentAdmin)
