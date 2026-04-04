from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request

from users.enums import UserRole, UserPermissions

from typing import cast, Collection

from users.models import CustomUser
from users.serializers import UpdateUserPermissionSerializer

__all__ = [
    'IsAdmin',
    'IsStaff',
    'HasUserPermission',
    'CanModifyPermissions',
    'SameLibraryObjectPermission',
]


def _get_by_lookup(obj: object, lookup: str) -> object | None:
    """Цепочка атрибутов как у Django lookup: ``staff_profile__library_branch_id``."""
    target: object | None = obj
    for name in lookup.split('__'):
        if target is None:
            return None
        target = getattr(target, name, None)
    return target


class HasRole(IsAuthenticated):
    allowed_roles = tuple()

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False

        return request.user.role in self.allowed_roles


class IsAdmin(HasRole):
    allowed_roles = (UserRole.Admin,)


class IsStaff(HasRole):
    allowed_roles = (UserRole.Admin.value, UserRole.Manager.value)


class HasUserPermission(BasePermission):
    code: UserPermissions

    def __init__(self, code: UserPermissions):
        self.code = code

    def has_permission(self, request, *args):
        return request.user.user_permissions.filter(code=self.code).exists()


class CanModifyPermissions(BasePermission):
    def has_permission(self, request: Request, view):
        serializer = UpdateUserPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_permissions = cast(Collection[int], serializer.validated_data['permissions'])

        user = cast(CustomUser, request.user)

        if not user or not user.is_authenticated:
            return False

        can_modify_admin_perms = user.user_permissions.filter(code=UserPermissions.EditAdminPermissions).exists()
        can_modify_manager_perms = can_modify_admin_perms or user.user_permissions.filter(
            code=UserPermissions.EditManagerOnlyPermissions).exists()

        update_manager_perms_attempt = False
        update_admin_perms_attempt = False

        for perm in updated_permissions:
            enum_perm = UserPermissions(perm)

            if enum_perm in CustomUser.admin_only_permissions:
                update_admin_perms_attempt = True
            else:
                update_manager_perms_attempt = True

        if update_admin_perms_attempt and not can_modify_admin_perms:
            return False

        if update_manager_perms_attempt and not can_modify_manager_perms:
            return False

        return True


class SameLibraryObjectPermission(BasePermission):
    """Сравнивает ``library_branch_id`` объекта и текущего пользователя по настраиваемым lookup."""

    def __init__(
        self,
        *,
        object_library_branch_lookup: str,
        user_library_branch_lookup: str = 'staff_profile__library_branch_id',
    ):
        self.object_library_branch_lookup = object_library_branch_lookup
        self.user_library_branch_lookup = user_library_branch_lookup

    def has_object_permission(self, request, view, obj):
        user = cast(CustomUser, request.user)
        if not user.is_authenticated:
            return False
        if user.is_admin:
            return True

        object_branch_id = _get_by_lookup(obj, self.object_library_branch_lookup)
        user_branch_id = _get_by_lookup(user, self.user_library_branch_lookup)

        if object_branch_id is None or user_branch_id is None:
            return False
        return object_branch_id == user_branch_id
