from __future__ import annotations

import datetime

from django.db.models import QuerySet, Q
from typing import TYPE_CHECKING

from work_reservations.enums import WorkReservationStatus
from common_core.queryset import QuerySetStaffLibraryScopedMixin

__all__ = ['WorkReservationQuerySet']

if TYPE_CHECKING:
    from work_reservations.models import WorkReservation

    class _Base(QuerySet[WorkReservation]):
        pass
else:
    class _Base(QuerySet):
        pass

class WorkReservationQuerySet(_Base, QuerySetStaffLibraryScopedMixin['WorkReservationQuerySet']):
    default_library_lookup = 'library_branch_id'

    class Filters:
        open = Q(status=WorkReservationStatus.Open)
        closed = Q(status=WorkReservationStatus.Closed)
        open_outdated = Q(open, reserved_till__lt=datetime.datetime.now().date())

    def filter_open(self) -> WorkReservationQuerySet:
        return self.filter(self.Filters.open)

    def filter_open_outdated(self) -> WorkReservationQuerySet:
        return self.filter(self.Filters.open_outdated)

    def filter_closed(self) -> WorkReservationQuerySet:
        return self.filter(self.Filters.closed)

    def filter_by_client(self, client_id: str):
        return self.filter(client_id=client_id)

    def filter_open_by_client(self, client_id: str):
        return self.filter_by_client(client_id).filter_open()

    def filter_open_outdated_by_client(self, client_id: str):
        return self.filter_by_client(client_id).filter_open_outdated()

    def filter_closed_by_client(self, client_id):
        return self.filter_by_client(client_id).filter_closed()

