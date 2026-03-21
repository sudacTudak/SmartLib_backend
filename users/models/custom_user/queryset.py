from __future__ import annotations
from collections.abc import Collection

from django.db.models import QuerySet, Count, Q

from users.enums import UserRole, UserPermissions

from django.core.exceptions import ObjectDoesNotExist
from typing import TYPE_CHECKING, TypeVar

__all__ = ['CustomUserQuerySet']

if TYPE_CHECKING:
    from .models import CustomUser

    class _Base(QuerySet[CustomUser]):
        pass
else:
    class _Base(QuerySet):
        pass

class CustomUserQuerySet(_Base):
    def get_library_managers(self, library_branch_id: str):
        return self.filter(staff_profile__library_branch=library_branch_id)

    def get_by_email(self, email: str) -> CustomUser | None:
        try:
            print('email: ', email)
            return self.get(email=email)
        except (ObjectDoesNotExist,):
            return None

    def get_by_id(self, user_id: str) -> CustomUser | None:
        try:
            return self.get(pk=user_id)
        except (ObjectDoesNotExist,):
            return None

    def get_all_by_role(self, role: UserRole):
        return self.all().filter(role=role.value)

    def get_clients(self):
        return self.get_all_by_role(UserRole.Client)

    def get_staff(self):
        return self.all().exclude(role=UserRole.Client.value)

    def get_all_by_permissions(self, permissions: Collection[UserPermissions]):
        if not permissions or len(permissions) == 0:
            return self

        permission_values = [p.value for p in permissions]

        return (
            self.annotate(
                matched_perms=Count(
                    'user_permissions',
                    filter=Q(user_permissions__code__in=permission_values),
                    distinct=True
                )
            )
            .filter(matched_perms=len(permission_values))
        )