from collections.abc import Collection

from django.db.models import QuerySet, Count, Q, Model

from users.enums import UserRole, UserPermissions

from django.core.exceptions import ObjectDoesNotExist

__all__ = ['CustomUserQuerySet']

class CustomUserQuerySet(QuerySet):
    def get_library_managers(self, library_branch_id: str):
        pass

    def get_by_email(self, email: str):
        try:
            return self.get(email=email)
        except (ObjectDoesNotExist,):
            return None

    def get_all_by_role(self, role: UserRole):
        return self.all().filter(role=role.value)

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
