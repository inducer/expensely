from django.shortcuts import render
from django.contrib.auth.decorators import (
        login_required)

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

import django.forms as forms

from expenses.models import (  # noqa
        Account, Entry, EntryComponent, EntryCategory,
        account_category)


class AddSimpleExpenseForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['valid_date', 'description']

    category = forms.ModelChoiceField(
            queryset=EntryCategory.objects,
                required=True)
    funding_source = forms.ModelChoiceField(
            queryset=Account.objects.filter(
                category=account_category.funding_source),
                required=True)
    amount = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"

        self.helper.add_input(
                Submit("submit", "Submit", css_class="col-lg-offset-2"))
        super(AddSimpleExpenseForm, self).__init__(*args, **kwargs)


@login_required
def add_simple_expense(request):
    if request.method == "POST":
        form = AddSimpleExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: Process data
            form = AddSimpleExpenseForm()
    else:
        form = AddSimpleExpenseForm()  # An unbound form

    return render(request, 'generic-form.html', {
        "form": form,
        "form_description": "Add Simple Expense",
    })
