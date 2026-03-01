from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

from users.enums import UserRole, Gender
from .manager import CustomUserManager
from users.models.permissions import CustomPermissionsMixin
from uuid import uuid4 as uuid

__all__ = ['CustomUser']


class CustomUser(AbstractBaseUser, CustomPermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    email = models.EmailField(unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True)

    gender = models.CharField(
        max_length=10,
        choices=Gender.as_django_model_choices(),
        default=Gender.Male
    )

    role = models.CharField(
        max_length=30,
        choices=UserRole.as_django_model_choices(),
        default=UserRole.Client
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects = CustomUserManager()
