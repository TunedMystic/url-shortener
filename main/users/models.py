from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        unique=True,
        max_length=200
    )
    first_name = models.CharField(
        _('first name'),
        max_length=100,
        blank=True
    )
    last_name = models.CharField(
        _('last name'),
        max_length=100,
        blank=True
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        )
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        )
    )

    def get_full_name(self):
        return ('{0} {1}').format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
