from typing import ClassVar

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils import timezone

from users.enums import UserRole, Gender
from .manager import CustomUserManager
from users.models.permissions import CustomPermissionsMixin
from uuid import uuid4 as uuid
from typing import Optional, cast, TYPE_CHECKING
from .constants import MAX_EMAIL_LENGTH

__all__ = ['CustomUser']


class CustomUser(AbstractBaseUser, CustomPermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid, editable=False)
    email = models.EmailField(unique=True, max_length=MAX_EMAIL_LENGTH)

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
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: ClassVar[list[str]] = []

    objects = CustomUserManager()

    if TYPE_CHECKING:
        from users.models import StaffProfile, UserProfile

        staff_profile: StaffProfile
        user_profile: Optional[UserProfile]

    class Meta:
        db_table = 'custom_user'
        ordering = ('created_at',)

    def __str__(self):
        username = super().__str__()
        return f'{self.id}_{username}'

    @property
    def is_staff_user(self):
        return UserRole(self.role).is_staff

    @property
    def is_manager(self):
        return UserRole(self.role) == UserRole.Manager

    @property
    def is_admin(self):
        return UserRole(self.role) == UserRole.Admin

    @property
    def library_branch_id(self):
        if not self.is_staff_user:
            raise ValueError(f'{self}: Роль пользователя не соответствует операции')
        if profile := getattr(self, 'staff_profile', None) is None:
            raise ValueError(f'{self}: Профиль сотрудника не найден')

        return cast(str, profile.library_branch_id)
