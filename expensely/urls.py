import re

import django.contrib.auth.views
from django.conf import settings
from django.contrib import admin
from django.urls import re_path
from django.views.generic import TemplateView

import expensely.views
import expenses.views


admin.autodiscover()

urlb = r"^%s" % re.escape(settings.DYNSITE_ROOT.lstrip("/"))

urlpatterns = [
    re_path(urlb + r"$", TemplateView.as_view(template_name="welcome.html")),
    re_path(urlb + r"admin/", admin.site.urls),
    re_path(
        urlb + r"tracking/add-simple-expense/$",
        expenses.views.add_simple_expense,
    ),
    re_path(
        urlb + r"reporting/accounts/$",
        expenses.views.list_accounts,
    ),
    re_path(
        urlb + r"reporting/account/(?P<id>[0-9]+)$",
        expenses.views.view_account,
        name="expensely-view_account",
    ),
    re_path(
        urlb + r"accounts/login/$",
        expensely.views.login,
    ),
    re_path(
        urlb + r"accounts/logout/$",
        django.contrib.auth.views.LogoutView.as_view(),
        {"template_name": "base.html"},
    ),
]
