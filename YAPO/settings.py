import os
import shutil
import sys

from configuration import Config, Constants

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "0px^lshd1lsf6uq#%90lre3$iqkz9=i7a0ko2_83b$n@=&(*d5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
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


# First of all, check if the db is located in the old folder (root)

if not 'migrat' or "passcheck" in str(sys.argv[1:]): # Check if the user runs migration. Don't execute this if that's the case.
    src = Config().root_path
    dest = os.path.join(Config().database_dir)
    okmoved = True

    try:
        # noinspection PyUnresolvedReferences
        if sys.frozen or sys.importers:
            compiled = True
    except AttributeError:
        compiled = False

    if not os.path.isfile(os.path.join(src, "db.sqlite3")) and not os.path.isfile(os.path.join(dest, "db.sqlite3")):
        print("\n")
        print("No database")
        print(f"There is no database installed at: {os.path.join(dest, 'db.sqlite3')}")
        print(
            "Please run the below commands from your YAPO main directory to create the database,\nor place your database at the above location.\n\nConsult the guide or website for help.")
        print("\nCOMMAND(S) TO RUN:\n")
        if not compiled:
            print("python manage.py makemigrations")
            print("python manage.py migrate\n")
        else:
            print("migrate.exe\n")
            print("(Follow the directions displayed)")
        input("\nPress enter to exit YAPO and take care of the above. >")
        sys.exit()

    if os.path.isfile(os.path.join(src, "db.sqlite3")):
        if not os.path.isfile(os.path.join(dest, "db.sqlite3")):
            try:
                shutil.move(src, dest)
                okmoved = True
            except:
                print("Error moving the database")
                print("There was an error moving the database to it's new location:")
                print(f"{src} -> {dest}")
                input("Please check the source and destination. Press enter to exit YAPO. >")
                sys.exit()
        else:
            print("Databases at two locations")
            print(f"There is a database file at both the below listed locations. You need to delete the one")
            print("you don't wish to use and make sure the other is in the listed destination directory.")
            print("This is a check because we have moved the database to a subdirectory.")
            print("")
            print(f"SOURCE: {src}")
            print(f"DESTINATION: {src}")
            input("Press enter to exit YAPO, and start it again when the above is taken care of. >")
            sys.exit()
        if okmoved:
            print(f"The database was moved to {dest}.")




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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
		'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(Config().data_path, 'server.log')
            },
        'logtodb': {
            'level': 'INFO',
            'class': 'videos.logtodb.logtodb'
        }
    },
    'loggers': {
        '': {
            'handlers' : [ "logtodb", 'file'],
            'propogate': True
        }
    }
}

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

# APPEND_SLASH = True

REST_FRAMEWORK = {
    #
    "DEFAULT_PAGINATION_CLASS": "YAPO.pagination.HeaderLimitOffsetPagination",
    "PAGE_SIZE": 500,
}
