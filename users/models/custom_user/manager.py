from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction

from users.enums import UserRole

from .queryset import CustomUserQuerySet

__all__ = ['CustomUserManager']


class CustomUserManager(BaseUserManager.from_queryset(CustomUserQuerySet)):
    def ensure_client_profile(self, user):
        """Создаёт UserProfile, если пользователь — клиент; иначе ValueError."""

        from users.models import UserProfile

        if UserRole(user.role) != UserRole.Client:
            raise ValueError('Профиль пользователя доступен только для роли client')
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    def _create_user(self, *, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        user = self._create_user(email=email, password=password, **extra_fields)
        if UserRole(user.role) == UserRole.Client:
            self.ensure_client_profile(user)
        return user

    @transaction.atomic
    def create_staff(self, *, email, password, profile_data, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not password:
            raise ValueError('Пароль обязателен')
        if not profile_data:
            raise ValueError('Не предоставлены данные профиля сотрудника')

        from users.models import StaffProfile

        user = self._create_user(email=email, password=password, **extra_fields)
        StaffProfile.objects.create(user=user, **profile_data)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def change_password(self, email, current_password, new_password):
        if not email:
            raise ValueError('Email is required')

        user = self.get_by_email(email=email)

        if user is None:
            raise ValueError('Пользоатель с таким Email не найден')

        if not user.check_password(current_password):
            raise ValueError('Текущий пароль неверный')

        user.set_password(new_password)
        user.save(using=self._db)
        return user
