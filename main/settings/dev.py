from .settings import *

DEBUG = True
DJANGO_LOG_LEVEL = "DEBUG"

EMAIL_FILE_PATH = BASE_DIR / "email"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
