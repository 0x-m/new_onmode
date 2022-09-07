import os

from .common import *

# -------------DJANGO BASIC SETTINGS -----------
SECRET_KEY = (
    "django-insecure-xty0%&omz0mo&f%69!_l%2nq(h0(oa^w7b%0$$8!(ts16$ei&!"
)
DEBUG = True
ALLOWED_HOSTS = ["localhost", "0.0.0.0"]
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

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
