import onmode.storage_backends as storage_backends
from decouple import Csv, config

# ---------------- DJANGO BASICS ---------
SECRET_KEY = config("SECRET_KEY")
DEBUG = False
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
# -----------------------------------------


# ---------------- S3 CONFIGURATION --------
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
# "https://s3.ir-thr-at1.arvanstorage.com"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}
# static file storage
STATIC_URL = f"https://{storage_backends.StaticStorage.custom_domain}/{storage_backends.StaticStorage.bucket_name}/"
STATICFILES_STORAGE = "onmode.storage_backends.StaticStorage"

# media file settings
# PUBLIC_MEDIA_LOCATION = 'mediabucket'
MEDIA_URL = f"https://{storage_backends.PublicMediaStorage.custom_domain}/{storage_backends.PublicMediaStorage.bucket_name}/"
DEFAULT_FILE_STORAGE = "onmode.storage_backends.PublicMediaStorage"

# ------------------------------------------

# ------------ DATABASES --------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER_NAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
# -------------------------------------------

IMPORT_EXPORT_USE_TRANSACTIONS = False


DEBUG_PROPAGATE_EXCEPTIONS = True

TINYMCE_JS_URL = "https://onmodestaticfiles.s3.ir-thr-at1.arvanstorage.com/static/tinymce/tinymce.min.js"
