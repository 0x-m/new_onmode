import os

from decouple import config

from .common import *

# -------------DJANGO BASIC SETTINGS -----------
SECRET_KEY = (
    "django-insecure-xty0%&omz0mo&f%69!_l%2nq(h0(oa^w7b%0$$8!(ts16$ei&!"
)
DEBUG = config("DEV_DEBUG", cast=bool)
ALLOWED_HOSTS = ["localhost", "0.0.0.0", ".vercel.app", ".now.sh"]
# ----------------------------------------------

# ------------ DJANGO CORS HEADERS --------------
CSRF_TRUSTED_ORGINS = ["http://localhost:3000"]
CORS_ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8000"]
# -----------------------------------------------

# ------------- DATABASES ------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# -------------------------------------------------
USE_S3 = config("USE_S3", default=False, cast=bool)


# if USE_S3:
#     AWS_ACCESS_KEY_ID = "afa9396c-f015-4a2f-9917-40d62c09646a"
#     AWS_SECRET_ACCESS_KEY = (
#         "e1e762f233a0877eb37f32e1ca721fb248b01535f3fa65c047e325653e5d94bd"
#     )

#     # AWS_STORAGE_BUCKET_NAME = 'mediabucket'
#     # AWS_S3_CUSTOM_DOMAIN = '%s.s3.ir-thr-at1.arvanstorage.com' % AWS_STORAGE_BUCKET_NAME
#     AWS_S3_OBJECT_PARAMETERS = {
#         "CacheControl": "max-age=86400",
#     }
#     AWS_S3_ENDPOINT_URL = "https://s3.ir-thr-at1.arvanstorage.com"
#     # static file storage
#     STATIC_URL = f"https://{storage_backends.StaticStorage.custom_domain}/{storage_backends.StaticStorage.bucket_name}/"
#     STATICFILES_STORAGE = "onmode.storage_backends.StaticStorage"

#     # media file settings
#     # PUBLIC_MEDIA_LOCATION = 'mediabucket'
#     MEDIA_URL = f"https://{storage_backends.PublicMediaStorage.custom_domain}/{storage_backends.PublicMediaStorage.bucket_name}/"
#     DEFAULT_FILE_STORAGE = "onmode.storage_backends.PublicMediaStorage"
# else:
#     STATIC_URL = "/static/"
#     STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#     MEDIA_URL = "/media/"
#     MEDIA_ROOT = os.path.join(BASE_DIR, "media")

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles_build", "static")  # vercel
# STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
