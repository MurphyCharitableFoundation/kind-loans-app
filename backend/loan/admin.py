"""Django admin customization."""

from django.contrib import admin, messages
from django.contrib.admin.options import (
    HttpResponseRedirect,
    csrf_protect_m,
    unquote,
)
from loan import models

from .services import (
    borrower_apply_repayments,
    borrower_make_payment,
    borrower_receive_payment,
)


class LoanProfileAdmin(admin.ModelAdmin):
    change_form_template = "admin/loan_profile_change_form.html"

    list_display = (
        "__str__",
        "target_amount",
        "sum_of_contributions",
        "sum_of_repayments",
        "city",
        "country",
    )
    readonly_fields = (
        "is_paid_raised_amount",
        "has_repaid",
        "sum_of_contributions",
        "sum_of_repayments",
    )

    actions = ["get_payment", "make_payment", "apply_repayments"]

    def get_payment(self, request, queryset):
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            borrower_receive_payment(obj)
            updated_count = 1
        else:
            list(
                map(
                    lambda borrower: borrower_receive_payment(borrower),
                    queryset,
                )
            )
            updated_count = queryset.count()

        msg = "Paid {} borrower(s) from respective contributions.".format(
            updated_count
        )
        self.message_user(request, msg, messages.SUCCESS)

    def make_payment(self, request, queryset):
        """Make payment for Loan Profile or several Loan Profiles."""
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            borrower_make_payment(obj)
            updated_count = 1
        else:
            list(
                map(lambda borrower: borrower_make_payment(borrower), queryset)
            )
            updated_count = queryset.count()

        msg = "Made loan repayment for {} borrower(s).".format(updated_count)
        self.message_user(request, msg, messages.SUCCESS)

    def apply_repayments(self, request, queryset):
        """Apply repayment for a LoanProfile or several Loan Profiles."""
        if isinstance(queryset, models.LoanProfile):
            obj = queryset
            borrower_apply_repayments(borrower=obj)
            updated_count = 1
        else:
            list(
                map(
                    lambda loan_profile: borrower_apply_repayments(
                        borrower=loan_profile
                    ),
                    queryset,
                )
            )
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
    readonly_fields = ["lender", "borrower", "amount"]


class RepaymentAdmin(admin.ModelAdmin):
    readonly_fields = ["borrower", "amount", "is_applied"]
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


admin.site.register(models.Category)
admin.site.register(models.LoanProfile, LoanProfileAdmin)

admin.site.register(models.Contribution, ContributionAdmin)
admin.site.register(models.Repayment, RepaymentAdmin)
