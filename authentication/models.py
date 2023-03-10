from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import EmailValidator

from .managers import UserManager

from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

auth_provider_choices = (
    ('email', 'email'),
    ('google', 'google'),
)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        _('email address'),
        max_length=255,
        unique=True,
        blank=False,
        help_text='Required. Add a valid email address',
        error_messages={
            'unique': 'A user with that email already exists.',
            'required': 'Email is required',
            'blank': 'Email is required',
            'invalid': 'Please Enter a Valid Email Address',
        }
    )
    auth_provider = models.CharField(
        _('authentication provider'),
        max_length=50,
        choices=auth_provider_choices,
        default='email',
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active status'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. Substitution for deleting accounts.'),
    )
    is_verified = models.BooleanField(
        _('verified status'),
        default=False,
        help_text=_('Designates whether this user has verified their email address.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('-date_joined',)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()
    
    def get_short_name(self):
        "Return the short name for the user."
        return self.first_name

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken().for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }