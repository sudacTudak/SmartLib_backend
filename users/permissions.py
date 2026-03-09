from rest_framework.permissions import BasePermission, IsAuthenticated
from users.enums import UserRole, UserPermissions

__all__ = ['IsAdmin', 'IsStaff', 'HasUserPermission']

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

