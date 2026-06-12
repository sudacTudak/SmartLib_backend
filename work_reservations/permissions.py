from rest_framework.permissions import BasePermission, IsAuthenticated

from users.enums import UserPermissions, UserRole
from users.permissions import HasUserPermission, IsStaff

__all__ = [
    'IsClient',
    'IsStaffOrReservationClient',
    'CanManageWorkReservations',
]


class IsClient(BasePermission):
    """Только пользователь с ролью client."""

    def has_permission(self, request, view):
        if not IsAuthenticated().has_permission(request, view):
            return False
        return UserRole(request.user.role).is_client


class IsStaffOrReservationClient(BasePermission):
    """Доступ к объекту брони: сотрудник или клиент-владелец."""

    def has_object_permission(self, request, view, obj):
        if not IsAuthenticated().has_permission(request, view):
            return False

        if IsStaff().has_permission(request, view):
            return True

        return getattr(obj, 'client_id', None) == getattr(request.user, 'id', None)


class CanManageWorkReservations(IsStaff):
    """Сотрудник с правом обработки броней (смена статуса и т.п.)."""

    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return HasUserPermission(UserPermissions.BookReservationManagement).has_permission(request, view)
