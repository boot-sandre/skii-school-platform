# flake8: noqa F403

from .settings import *
from .dev import *  # Share things on dev and version them

INSTALLED_APPS += [
    "django_extensions",
]

DEBUG = True
DJANGO_LOG_LEVEL = "DEBUG"
