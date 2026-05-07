from __future__ import annotations

from django.db.models import QuerySet

from users.models import CustomUser

__all__ = ['scope_library_branch_filters']


def scope_library_branch_filters(qs: QuerySet, *, user: CustomUser, library_branch_lookup: str) -> QuerySet:
    if user.is_admin:
        return qs
    profile = getattr(user, 'staff_profile', None)
    if profile is None or profile.library_branch_id is None:
        return qs.none()
    return qs.filter(**{library_branch_lookup: profile.library_branch_id})
