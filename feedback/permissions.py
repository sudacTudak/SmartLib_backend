from rest_framework.permissions import BasePermission, IsAuthenticated

from users.permissions import IsStaff

__all__ = ['IsStaffOrFeedbackOwner']


class IsStaffOrFeedbackOwner(BasePermission):
    """PATCH/DELETE: только staff **или** автор отзыва."""

    def has_object_permission(self, request, view, obj):
        if not IsAuthenticated().has_permission(request, view):
            return False

        if IsStaff().has_permission(request, view):
            return True

        return getattr(obj, 'client_id', None) == getattr(request.user, 'id', None)
