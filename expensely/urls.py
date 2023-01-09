from django.urls import re_path
from django.conf import settings
import django.contrib.auth.views
import expenses.views
import expensely.views

from django.views.generic import TemplateView

import re

from django.contrib import admin
admin.autodiscover()

urlb = r"^%s" % re.escape(settings.DYNSITE_ROOT.lstrip("/"))

urlpatterns = [
    re_path(urlb+r'$', TemplateView.as_view(template_name='welcome.html')),

    re_path(urlb+r'admin/', admin.site.urls),

    re_path(urlb+r'tracking/add-simple-expense/$', expenses.views.add_simple_expense,),

    re_path(urlb+r'reporting/accounts/$', expenses.views.list_accounts,),
    re_path(urlb+r'reporting/account/(?P<id>[0-9]+)$',
        expenses.views.view_account,
        name="expensely-view_account"),

    re_path(urlb+r'accounts/login/$', expensely.views.login,),
    re_path(urlb+r'accounts/logout/$',
        django.contrib.auth.views.LogoutView.as_view(),
        {'template_name': 'base.html'}),
    ]
