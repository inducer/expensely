from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import (
        login_required)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages
from django.db import transaction

import django.forms as forms

from expenses.models import (  # noqa
        Account, Entry, EntryComponent, EntryCategory, EntryComment,
        account_category)


class AddSimpleExpenseForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['valid_date', 'description', 'category']

    funding_source = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.funding_source),
                required=True)
    amount = forms.DecimalField(max_digits=19, decimal_places=2, required=True)
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
                Submit("submit", "Submit", css_class="col-lg-offset-2"))
        super(AddSimpleExpenseForm, self).__init__(*args, **kwargs)


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
            entry.save()
            funding = EntryComponent(
                    entry=entry,
                    account=form.cleaned_data["funding_source"],
                    amount=-form.cleaned_data["amount"],
                    )
            funding.save()

            from decimal import Decimal

            TWO_PLACES = Decimal(10) ** -2
            frac1 = Decimal(form.cleaned_data["fraction_1"])
            frac2 = Decimal(form.cleaned_data["fraction_2"])

            total_fraction = frac1 + frac2
            total_amount = Decimal(form.cleaned_data["amount"]).quantize(TWO_PLACES)
            amount_1 = (total_amount * frac1 / total_fraction).quantize(TWO_PLACES)
            amount_2 = total_amount - amount_1

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

            if form.cleaned_data["comment"]:
                comment = EntryComment(
                        entry=entry,
                        creator=request.user,
                        comment=form.cleaned_data["comment"]
                        )
                comment.save()

            messages.add_message(request, messages.INFO, 'Expense added.')
            form = empty_form()
    else:
        form = empty_form()  # An unbound form

    return render(request, 'generic-form.html', {
        "form": form,
        "form_description": "Add Simple Expense",
    })


@login_required
def list_accounts(request):
    return render(request, 'expenses/account-list.html', {
        "accounts": Account.objects.all()
        .order_by("group__name", "symbol"),
    })


@login_required
def view_account(request, id):
    account = get_object_or_404(Account, pk=id)

    from decimal import Decimal
    TWO_PLACES = Decimal(10) ** -2

    def gen_tallies():
        tally = Decimal(0)
        for tx in (account.entry_components
                .order_by("entry__valid_date").all()):
            tally += Decimal(tx.amount)
            tally = tally.quantize(TWO_PLACES)

            yield (tx, tally)

    return render(request, 'expenses/account-view.html', {
        "account": account,
        "transactions": gen_tallies()
    })
