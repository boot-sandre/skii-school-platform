# flake8: noqa
from .settings import *

DEBUG = True

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
        },
    }
}

DJANGO_LOG_LEVEL = "INFO"
DJANGO_LOG_SQL_LEVEL = "INFO"
# Python logging
LOGGING.update(
    {
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
        "loggers": {
            "skii": {
                "level": DJANGO_LOG_LEVEL,
            },
            "django": {
                "level": DJANGO_LOG_LEVEL,
            },
            "tests": {
                "level": DJANGO_LOG_LEVEL,
            },
            "django.server": {
                "handlers": ["console"],
                "level": DJANGO_LOG_LEVEL,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console"],
                "level": DJANGO_LOG_LEVEL,
                "propagate": False,
            },
            "django.template": {
                "level": DJANGO_LOG_LEVEL,
                "propagate": True,
            },
            "django.db.backends": {
                "level": DJANGO_LOG_SQL_LEVEL,
                "propagate": True,
            },
            "django.security": {
                "level": DJANGO_LOG_LEVEL,
                "propagate": True,
            },
            "django.utils.autoreload": {
                "handlers": ["null"],
                "level": "NOTSET",
                "propagate": False,
            },
            # Divers python loggers
            "py.warnings": {
                "handlers": ["null"],
                "level": "NOTSET",
                "propagate": False,
            },
            "parso": {
                "level": "INFO",
                "propagate": True,
            },
            "faker.factory": {"level": "INFO", "propagate": True},
            "factory.generate": {"level": "INFO", "propagate": True},
        },
    }
)
