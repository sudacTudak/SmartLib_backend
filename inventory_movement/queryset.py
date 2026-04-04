from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import QuerySet

__all__ = ['InventoryMovementQuerySet']

if TYPE_CHECKING:
    from users.models import CustomUser

    from inventory_movement.models import InventoryMovement

    class _Base(QuerySet[InventoryMovement]):
        pass
else:
    class _Base(QuerySet):
        pass


class InventoryMovementQuerySet(_Base):
    def scoped_for_staff_same_library(self, user: "CustomUser") -> InventoryMovementQuerySet:
        """Админ — вся выборка; менеджер — только движения своей библиотеки."""
        if user.is_admin:
            return self
        profile = getattr(user, 'staff_profile', None)
        if profile is None or profile.library_branch_id is None:
            return self.none()
        return self.filter(library_branch_id=profile.library_branch_id)
