from .settings import *  # noqa
import os

DEBUG = True
DJANGO_LOG_LEVEL = "DEBUG"

EMAIL_FILE_PATH = BASE_DIR / "email"  # noqa
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"

INSTALLED_APPS += [  # noqa
    "django_extensions",
]


DJANGO_LOG_LEVEL = os.environ.get(
    "DJANGO_LOG_LEVEL", default="DEBUG" if DEBUG else "INFO"
)
LOGGING.update(     # noqa
    {  # noqa
        "root": {
            "handlers": ["console"],
            "level": DJANGO_LOG_LEVEL,
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
                "level": "INFO",
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
