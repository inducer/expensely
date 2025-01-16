from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth.forms import AuthenticationForm as AuthenticationFormBase


class AuthenticationForm(AuthenticationFormBase):
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-lg-2"
        self.helper.field_class = "col-lg-8"

        self.helper.add_input(
                Submit("submit", "Sign in"))
        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["autofocus"] = "autofocus"


def login(request):
    from django.contrib.auth.views import LoginView
    return LoginView.as_view(template_name="generic-form.html",
            authentication_form=AuthenticationForm)(request)
