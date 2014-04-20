from django.shortcuts import render
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
            # TODO: Process data
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

            total_fraction = (
                    form.cleaned_data["fraction_1"]
                    + form.cleaned_data["fraction_2"])

            amount_1 = (
                    form.cleaned_data["amount"] * form.cleaned_data["fraction_1"]
                    / total_fraction)
            amount_2 = form.cleaned_data["amount"] - amount_1

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
