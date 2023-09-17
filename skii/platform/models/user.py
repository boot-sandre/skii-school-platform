from typing import List

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models import Manager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from email_validator.validate_email import validate_email as email_validator


class UserSkiiManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.objects.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class SkiiUser(AbstractBaseUser, PermissionsMixin):
    """User customized.

    - Use email field as django username. (USERNAME_FIELD)
    - Email fields have to be unique
    - Other fields can be change/overwrite
    """

    EMAIL_FIELD: str = "email"
    USERNAME_FIELD: str = EMAIL_FIELD
    REQUIRED_FIELDS: List[str] = []

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = _("Skii platform user")
        verbose_name_plural = _("Skii platform user(s)s")
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                name="unique_email_constraint",
            )
        ]
        abstract = False

    objects: Manager = UserSkiiManager()

    validators = [email_validator]

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    email = models.EmailField(
        _("Mail"),
        unique=True,
        null=False,
        blank=False,
        editable=True,
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    # username = models.Field(alias="email")
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    def get_absolute_url(self) -> str:
        """Return skii api url."""
        return "/skii/user/%i/" % self.pk

    def natural_key(self) -> tuple[str]:
        """Define a natural primary key.

        Limit id/uuid exchange between front/back.
        """
        return (self.get_username(),)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.get_username())

    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short/first name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Email this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
