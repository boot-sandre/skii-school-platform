from .settings import BASE_DIR

DEBUG = True
DJANGO_LOG_LEVEL = "INFO"

EMAIL_FILE_PATH = BASE_DIR / "email"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
