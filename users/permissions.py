from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request

from users.enums import UserRole, UserPermissions

from typing import cast, Collection

from users.models import CustomUser
from users.serializers import UpdateUserPermissionSerializer

__all__ = ['IsAdmin', 'IsStaff', 'HasUserPermission', 'CanModifyPermissions']


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
