from .settings import *     # noqa

DEBUG = True
DJANGO_LOG_LEVEL = "DEBUG"

EMAIL_FILE_PATH = BASE_DIR / "email"    # noqa
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

INSTALLED_APPS += [     # noqa
    "django_extensions",
]
