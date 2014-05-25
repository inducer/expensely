from django.conf.urls import patterns, include, url
from django.conf import settings

#import expensely.responders

from django.contrib import admin
admin.autodiscover()

import re

urlb = r"^%s" % re.escape(settings.DYNSITE_ROOT.lstrip("/"))
#urlb = "^"

from django.views.generic import TemplateView

urlpatterns = patterns('',
    (urlb+r'$', TemplateView.as_view(template_name='welcome.html')),

    url(urlb+r'admin/', include(admin.site.urls)),

    (urlb+r'tracking/add-simple-expense/$', 'expenses.views.add_simple_expense',),

    (urlb+r'reporting/accounts/$', 'expenses.views.list_accounts',),
    (urlb+r'reporting/account/(?P<id>[0-9]+)$',
        'expenses.views.view_account',),

    (urlb+r'accounts/login/$', 'expensely.views.login',),
    (urlb+r'accounts/logout/$',
        'django.contrib.auth.views.logout',
        {'template_name': 'base.html'}),
)
