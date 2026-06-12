from __future__ import annotations
from django.db.models import QuerySet
from typing import cast, TYPE_CHECKING, TypeVar, Any, Generic

__all__ = ['QuerySetStaffLibraryScopedMixin']

QuerySetT = TypeVar("QuerySetT", bound=QuerySet[Any])

class QuerySetStaffLibraryScopedMixin(Generic[QuerySetT]):
    default_library_lookup = None

    if TYPE_CHECKING:
        from users.models import CustomUser

        def scoped_for_staff_same_library(self, user: CustomUser, *, library_lookup: str | None = None) -> QuerySetT: ...

    def scoped_for_staff_same_library(self, user, *, library_lookup: str | None = None) -> QuerySetT:
        qs = cast(QuerySetT, cast(object, self))
        if not user.is_staff:
            raise PermissionError('Пользователь не менеджер')

        # Для админа разрешаем полный queryset
        if user.is_admin:
            return qs

        lookup = library_lookup or self.default_library_lookup

        if not lookup:
            raise ValueError('library_lookup не указан')

        staff_library_id = user.staff_profile.library_branch_id
        return qs.filter({[lookup]: staff_library_id})
