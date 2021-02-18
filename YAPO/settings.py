import json
import os
import re
import sys
from configuration import Config, Constants
from utils.printing import Logger
from datetime import datetime
import videos.const
import shutil
import colorama
log = Logger()
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0px^lshd1lsf6uq#%90lre3$iqkz9=i7a0ko2_83b$n@=&(*d5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
LOGGING_CONFIG = None
# SILENCED_SYSTEM_CHECKS = ["fields.W340"]
ALLOWED_HOSTS = ['*']
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
AUTOCOMMIT = True
TEST_MEMCACHE = False

if not DEBUG or TEST_MEMCACHE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    "django.contrib.admin.apps.SimpleAdminConfig",  # was 'django.contrib.admin'
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django_extensions",
    # 'selectable',
    "videos.apps.VideosConfig",
    "mptt",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    #    "django.contrib.auth.middleware.SessionAuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "YAPO.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
            "libraries": {
                # Adding this section should work around the issue. (https://github.com/pyinstaller/pyinstaller/issues/1717)
                # (This is for pyinstaller to recognize staticfiles tag
                "staticfiles": "django.templatetags.static",
                "i18n": "django.templatetags.i18n",
            },
        },
    },
]

WSGI_APPLICATION = "YAPO.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Config().database_path,
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    { "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", },
    { "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator", },
    { "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator", },
]

# Internationalization

LANGUAGE_CODE = "en-us"
# TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
# USE_TZ = True

# Static files (CSS, JavaScript, Images)
#These are moved to YML configuration, but retrieved here as constants

SITE_ROOT = Config().site_path
STATIC_ROOT = Config().site_static_path
STATIC_URL = f"/{Constants().site_static_subdir}/"
BASE_URL = "/"

MEDIA_ROOT = Config().site_media_path
MEDIA_URL = f"/{Constants().site_media_subdir}/"


IGNORABLE_404_URLS = [
    re.compile(r'[^\\s]+(.*?)\\.(jpg|jpeg|png|gif|JPG|JPEG|PNG|GIF)$'),
]

LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'ERROR',
            'class': 'django.utils.log.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['null', 'default'],
            'level': 'ERROR',
            'propagate': False,
        },
#        'requests': {
#            # The requests library is too verbose in it's logging, reducing the verbosity in our logs.
#            'handlers': ['null', 'default'],
#            'level': 'WARNING',
#            'propagate': True,
#        },
#        'urllib3': {
#            'handers': ['null', 'default'],
#            'level': 'WARNING',
#            'propagate': True
#        },
    }
}
# APPEND_SLASH = True

REST_FRAMEWORK = {
    #
    "DEFAULT_PAGINATION_CLASS": "YAPO.pagination.HeaderLimitOffsetPagination",
    "PAGE_SIZE": 500,
}
