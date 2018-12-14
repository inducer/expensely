from django.conf.urls import include, url
from django.conf import settings
import django.contrib.auth.views
import expenses.views
import expensely.views

from django.views.generic import TemplateView

import re

# import expensely.responders

from django.contrib import admin
admin.autodiscover()

urlb = r"^%s" % re.escape(settings.DYNSITE_ROOT.lstrip("/"))

urlpatterns = [
    url(urlb+r'$', TemplateView.as_view(template_name='welcome.html')),

    url(urlb+r'admin/', admin.site.urls),

    url(urlb+r'tracking/add-simple-expense/$', expenses.views.add_simple_expense,),

    url(urlb+r'reporting/accounts/$', expenses.views.list_accounts,),
    url(urlb+r'reporting/account/(?P<id>[0-9]+)$',
        expenses.views.view_account,
        name="expensely-view_account"),

    url(urlb+r'accounts/login/$', expensely.views.login,),
    url(urlb+r'accounts/logout/$',
        django.contrib.auth.views.LogoutView.as_view(),
        {'template_name': 'base.html'}),
    ]
