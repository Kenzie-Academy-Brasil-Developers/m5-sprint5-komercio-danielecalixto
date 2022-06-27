from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import BooleanField
from .utils import CustomUserManager
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(unique=False, null=True, max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    updated_at = models.DateTimeField(default=timezone.now)
    is_seller = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'is_seller']
    objects = CustomUserManager()