# flake8: noqa
from .settings import *

DEBUG = True
DJANGO_LOG_LEVEL = "DEBUG"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
DEFAULT_FROM_EMAIL = "test@test.com"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "skii.sqlite3",
        "TEST": {
            "NAME": BASE_DIR / "skii.test.sqlite3",
        }
    }
}
