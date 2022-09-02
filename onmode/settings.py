from pathlib import Path
import os
import sys
from decouple import config

from . import storage_backends

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config(
    "SECRET_KEY"
)  #'django-insecure-xty0%&omz0mo&f%69!_l%2nq(h0(oa^w7b%0$$8!(ts16$ei&!'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "storages",
    "tinymce",
    "gtm",
    "import_export",
    "django_filters",
    "jalali_date",
    "users",
    "django.contrib.admin",
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "storages",
    "tinymce",
    "gtm",
    "import_export",
    "django_filters",
    "jalali_date",
    "apps.users",
    "apps.catalogue",
    "apps.promotions",
    "apps.index",
    "apps.orders",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "onmode.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # "apps.catalogue.context_processors.CategoryContextProcessor",
                "apps.index.context_processors.info",
            ],
        },
    },
]

WSGI_APPLICATION = "onmode.wsgi.application"
ALLOW_UNICODE_SLUGS = True


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}

AUTH_USER_MODEL = "users.user"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "apps.users.OTP.OTPAuthenticationBackend",
]

LANGUAGE_CODE = "en-us"
LANGUAGES = [("en-us", "english"), ("fa-ir", "persian")]
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


JALALI_DATE_DEFAULTS = {
    "Strftime": {
        "date": "%y/%m/%d",
        "datetime": "%H:%M:%S _ %y/%m/%d",
    },
    "Static": {
        "js": [
            # loading datepicker
            "admin/js/django_jalali.min.js",
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        "css": {
            "all": [
                "admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css",
            ]
        },
    },
}

TINYMCE_DEFAULT_CONFIG = {
    "theme": "silver",
    "height": 400,
    "menubar": True,
    "language": "fa_ir",
    "directionality": "rtl",
    "plugins": "advlist,autolink,lists,directionality,link,image,charmap,print,preview,anchor"
    "searchreplace,visualblocks,code,fullscreen,insertdatetime,media,table,paste,"
    "code,help,wordcount",
    "toolbar": "undo redo | formatselect |ltr rtl"
    "bold italic backcolor | alignleft aligncenter "
    "alignright alignjustify | bullist numlist outdent indent | "
    "removeformat | help |  ",
}


TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_L10N = True
USE_TZ = True

USE_I18N = True

USE_TZ = True


# Cloud Storage Configurations----------------------
USE_S3 = False  # config('USE_S3',default=False, cast=bool)


import os


if USE_S3:
    AWS_ACCESS_KEY_ID = "afa9396c-f015-4a2f-9917-40d62c09646a"
    AWS_SECRET_ACCESS_KEY = (
        "e1e762f233a0877eb37f32e1ca721fb248b01535f3fa65c047e325653e5d94bd"
    )
    # AWS_STORAGE_BUCKET_NAME = 'mediabucket'
    # AWS_S3_CUSTOM_DOMAIN = '%s.s3.ir-thr-at1.arvanstorage.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
    AWS_S3_ENDPOINT_URL = "https://s3.ir-thr-at1.arvanstorage.com"
    # static file storage
    STATIC_URL = f"https://{storage_backends.StaticStorage.custom_domain}/{storage_backends.StaticStorage.bucket_name}/"
    STATICFILES_STORAGE = "onmode.storage_backends.StaticStorage"

    # media file settings
    # PUBLIC_MEDIA_LOCATION = 'mediabucket'
    MEDIA_URL = f"https://{storage_backends.PublicMediaStorage.custom_domain}/{storage_backends.PublicMediaStorage.bucket_name}/"
    DEFAULT_FILE_STORAGE = "onmode.storage_backends.PublicMediaStorage"
else:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATICFILES_DIRS = [BASE_DIR / "static"]
