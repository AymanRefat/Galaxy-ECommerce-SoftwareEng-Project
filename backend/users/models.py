from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class UserType(models.TextChoices):
        CONSUMER = 'CONSUMER', _('Consumer')
        VENDOR = 'VENDOR', _('Vendor')
        ADMIN = 'ADMIN', _('Admin')
        
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.CONSUMER,
    )
    social_provider = models.CharField(max_length=50, blank=True, null=True)
    social_id = models.CharField(max_length=100, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
