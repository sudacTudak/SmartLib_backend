from django.contrib.auth.base_user import BaseUserManager

from .queryset import CustomUserQuerySet

__all__ = ['CustomUserManager']


class CustomUserManager(BaseUserManager.from_queryset(CustomUserQuerySet)):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
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
