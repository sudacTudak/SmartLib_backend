from typing import TypeVar

from django.db.models.manager import Manager

from .queryset import AmenityQuerySet

__all__ = ['AmenityManager', 'AmenityManagerType']

class _AmenityManager(Manager, AmenityQuerySet):
    pass

AmenityManagerType = TypeVar('AmenityManagerType', bound=_AmenityManager)
AmenityManager = Manager.from_queryset(AmenityQuerySet)
