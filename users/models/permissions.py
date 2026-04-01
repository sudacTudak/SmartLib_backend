from django.contrib.auth.models import PermissionsMixin
from django.db import models
from uuid import uuid4 as uuid
from users.enums import UserPermissions

__all__ = ['UserPermission', 'CustomPermissionsMixin']


class UserPermission(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid,
        editable=False
    )
    code = models.PositiveIntegerField(choices=UserPermissions.as_django_model_choices())

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "user_permission"
        ordering = ["id"]

    def __str__(self):
        name = UserPermissions(self.code).name
        return f'{name} ({self.code})'


class CustomPermissionsMixin(PermissionsMixin):
    is_superuser = models.BooleanField(default=False)
    user_permissions = models.ManyToManyField(
        "users.UserPermission",
        blank=True,
        related_name="users",
    )

    admin_only_permissions = (UserPermissions.ManagerAdministration, UserPermissions.ManagerModification,
                              UserPermissions.EditManagerOnlyPermissions, UserPermissions.EditAdminPermissions)

    class Meta:
        abstract = True

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        if isinstance(perm, int):
            return self.user_permissions.filter(id=perm).exists()

        return False

    def has_module_perms(self):
        return True
