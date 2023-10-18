"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
VAR_DIR = BASE_DIR / "var"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-c5ny1qhpz*3o%@-nchet4ohg=wb4)*)$1y_g4w_8vcuu2#f$ga"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_countries",
    "djmoney",
    # Project generic apps
    "apps.base",
    "apps.account",
    "apps.doc",
    # Skii platform apps
    "skii.platform",
    "skii.endpoint",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "main.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "main" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "main.wsgi.application"

# Python logging

DJANGO_LOG_LEVEL = "INFO"
DJANGO_LOG_SQL_LEVEL = "INFO"
DJANGO_LOG_LEVEL = os.environ.get(
    "DJANGO_LOG_LEVEL", default=DJANGO_LOG_LEVEL
)
DJANGO_LOG_SQL_LEVEL = os.environ.get(
    "DJANGO_LOG_SQL_LEVEL", default=DJANGO_LOG_SQL_LEVEL
)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
        "verbose": {
            "format": "[{levelname:6}] {name:30} {message}",
            "style": "{",
            "fmt": "%Y-%m-%d %H:%M:%S",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{status_code:6}] [{asctime}] {name:30} {message}",
            "style": "{",
            "fmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "null": {
            "class": "logging.NullHandler",
        },
        "django.commands": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": sys.stdout,
        },
    },
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
            "handlers": ["django.server"],
            "level": DJANGO_LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["django.server"],
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
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
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


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = VAR_DIR / "static"
STATICFILES_DIRS = [
    BASE_DIR / "main" / "webapp_statics",
]
MEDIA_ROOT = VAR_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SAMESITE = "Lax"
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS
