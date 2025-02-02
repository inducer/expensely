from decimal import Decimal

import django.forms as forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.forms import DateInput
from django.shortcuts import get_object_or_404, render

from expenses.models import (
    Account,
    Entry,
    EntryComment,
    EntryComponent,
    account_category,
)


TWO_PLACES = Decimal(10) ** -2


class AddSimpleExpenseForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["valid_date", "description", "category"]

        widgets = {
                "valid_date": DateInput(attrs={"type": "date"}),
                }

    funding_source = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.funding_source),
            required=True)
    amount = forms.DecimalField(max_digits=19, decimal_places=2, required=True)
    discount_in_percent = forms.DecimalField(max_digits=19, decimal_places=2,
            required=False)
    funding_source = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.funding_source),
            required=True)

    fraction_1 = forms.IntegerField(required=True, initial=50)
    target_1 = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.expenses),
            required=True)

    fraction_2 = forms.IntegerField(required=True, initial=50)
    target_2 = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.expenses),
            required=True)

    comment = forms.CharField(required=False, widget=forms.widgets.Textarea)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"

        self.helper.add_input(
                Submit("submit", "Submit"))
        super().__init__(*args, **kwargs)


@login_required
@transaction.atomic
def add_simple_expense(request):
    def empty_form():
        frm = AddSimpleExpenseForm()
        return frm

    if request.method == "POST":
        form = AddSimpleExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            entry = Entry(
                    valid_date=form.cleaned_data["valid_date"],
                    description=form.cleaned_data["description"],
                    category=form.cleaned_data["category"],
                    creator=request.user,
                    )

            # This sends no email, because no components are created yet.
            # The signal handler is called explicitly below.
            entry.save()

            from decimal import Decimal

            TWO_PLACES = Decimal(10) ** -2  # noqa: N806
            frac1 = Decimal(form.cleaned_data["fraction_1"])
            frac2 = Decimal(form.cleaned_data["fraction_2"])

            total_fraction = frac1 + frac2
            total_amount = Decimal(form.cleaned_data["amount"])

            discount_percent = form.cleaned_data["discount_in_percent"]
            if discount_percent:
                discounted_amount = \
                        total_amount * Decimal(1-float(discount_percent)*0.01)
            else:
                discounted_amount = total_amount

            total_amount = total_amount.quantize(TWO_PLACES)
            discounted_amount = Decimal(discounted_amount).quantize(TWO_PLACES)
            discount_amount = total_amount - discounted_amount

            amount_1 = \
                    (discounted_amount * frac1 / total_fraction).quantize(TWO_PLACES)
            amount_2 = discounted_amount - amount_1

            funding = EntryComponent(
                    entry=entry,
                    account=form.cleaned_data["funding_source"],
                    amount=-discounted_amount,
                    )
            funding.save()
            if amount_1:
                target_1 = EntryComponent(
                        entry=entry,
                        account=form.cleaned_data["target_1"],
                        amount=amount_1,
                        )
                target_1.save()

            if amount_2:
                target_2 = EntryComponent(
                        entry=entry,
                        account=form.cleaned_data["target_2"],
                        amount=amount_2,
                        )
                target_2.save()

            if discount_percent:
                comment = EntryComment(
                        entry=entry,
                        creator=request.user,
                        comment="%.2f%% discount (%s) taken off %s."
                        % (discount_percent, discount_amount, total_amount)
                        )
                comment.save()

            if form.cleaned_data["comment"]:
                comment = EntryComment(
                        entry=entry,
                        creator=request.user,
                        comment=form.cleaned_data["comment"]
                        )
                comment.save()

            # Call signal handler to actually send notification email.
            from expenses.signals import entry_saved
            entry_saved(Entry, entry, created=True, raw=False)

            messages.add_message(request, messages.INFO, "Expense added.")
            form = empty_form()
    else:
        form = empty_form()  # An unbound form

    return render(request, "generic-form.html", {
        "form": form,
        "form_description": "Add Simple Expense",
    })


@login_required
def list_accounts(request):
    return render(request, "expenses/account-list.html", {
        "accounts": Account.objects.all()
        .order_by("group__name", "symbol"),
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id)

    def gen_tallies():
        tally = Decimal(0)
        for tx in (account.entry_components
                .order_by("entry__valid_date").all()):
            tally += Decimal(tx.amount)
            tally = tally.quantize(TWO_PLACES)

            yield (tx, tally)

    return render(request, "expenses/account-view.html", {
        "account": account,
        "transactions": reversed(list(gen_tallies()))
    })
