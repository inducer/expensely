"""
Django settings for expensely project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

from os.path import join

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

local_settings = {}
try:
    with open(join(BASE_DIR, "local_settings.py")) as inf:
        local_settings_contents = inf.read()
except IOError:
    pass
else:
    exec(compile(local_settings_contents, "local_settings.py", "exec"),
            local_settings)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '<OVERRIDDEN BY local_settings below>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'expenses',
    'crispy_forms',
    "bootstrap3_datetime",
)

CRISPY_TEMPLATE_PACK = "bootstrap3"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "DIRS": (
            join(BASE_DIR, "expensely", "templates"),
            ),
        "OPTIONS": {
            "context_processors": (
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",

                "expensely.util.add_root_url_to_template",
                ),
            },
        }
    ]

STATICFILES_DIRS = (
        join(BASE_DIR, "expensely", "static"),
        )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
)

ROOT_URLCONF = 'expensely.urls'

WSGI_APPLICATION = 'expensely.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# default, likely overriden by local_settings below
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

DYNSITE_ROOT = "/expensely/"

STATIC_URL = DYNSITE_ROOT + "static/"
STATIC_ROOT = join(BASE_DIR, "static")

LOGIN_URL = DYNSITE_ROOT + "accounts/login"
LOGIN_REDIRECT_URL = DYNSITE_ROOT

SESSION_COOKIE_NAME = 'expensely_sessionid'
SESSION_COOKIE_AGE = 12096000 # 20 weeks

for name, val in local_settings.iteritems():
    if not name.startswith("_"):
        globals()[name] = val
