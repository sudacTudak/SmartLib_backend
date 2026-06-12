from __future__ import annotations

import datetime
import random
from collections.abc import Callable, Generator
from typing import TYPE_CHECKING, cast

from django.db.models import Manager
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from work_reservations.enums import WorkReservationStatus
from work_reservations.models.reservation.model_config import WorkReservationModelConfig
from work_reservations.models.reservation.queryset import WorkReservationQuerySet

if TYPE_CHECKING:
    from users.models import CustomUser
    from work_reservations.models import WorkReservation

__all__ = ['WorkReservationManager']

_TERMINAL_TRANSITIONS = {
    WorkReservationStatus.Closed,
    WorkReservationStatus.ClientDeclined,
    WorkReservationStatus.StaffDeclined,
}

_STAFF_TERMINAL_STATUSES = frozenset({
    WorkReservationStatus.Closed,
    WorkReservationStatus.StaffDeclined,
})


def random_unique_factory(
    *,
    min_value: int,
    max_value: int,
) -> Callable[[], Generator[int, None, None]]:
    if min_value > max_value:
        raise ValueError('min_val не может быть больше max_val')
    generated: set[int] = set()
    total = max_value - min_value + 1

    def random_generator() -> Generator[int, None, None]:
        while len(generated) < total:
            num = random.randint(min_value, max_value)
            if num in generated:
                continue
            generated.add(num)
            yield num

    return random_generator


class WorkReservationManager(Manager.from_queryset(WorkReservationQuerySet)):
    def create_reservation(self, **created_data):
        unique_number_generator = random_unique_factory(
            min_value=WorkReservationModelConfig.MIN_UNIQUE_INDEX,
            max_value=WorkReservationModelConfig.MAX_UNIQUE_INDEX,
        )
        created_data['index'] = next(unique_number_generator())
        created_data.setdefault('status', WorkReservationStatus.Open.value)

        reservation = self.model(**created_data)
        reservation.save()
        return reservation

    def change_status(
        self,
        reservation: WorkReservation,
        *,
        new_status: WorkReservationStatus,
        actor: CustomUser,
    ) -> WorkReservation:
        reservation = cast('WorkReservation', reservation)
        current_status = WorkReservationStatus(reservation.status)

        if not current_status.is_open():
            raise ValidationError({'nonFieldErrors': ['Статус можно изменить только у открытой брони.']})

        if new_status == WorkReservationStatus.Open:
            raise ValidationError({'status': ['Бронь уже открыта.']})

        if new_status not in _TERMINAL_TRANSITIONS:
            raise ValidationError({'status': ['Недопустимый статус.']})

        if new_status == WorkReservationStatus.ClientDeclined:
            if str(reservation.client_id) != str(actor.id):
                raise ValidationError({'status': ['Отклонить бронь может только её владелец.']})
        elif not actor.is_staff_user:
            raise ValidationError({'status': ['Этот статус может установить только сотрудник.']})
        else:
            reservation.responsible_staff = actor

        if new_status in _STAFF_TERMINAL_STATUSES and reservation.responsible_staff_id is None:
            raise ValidationError({'nonFieldErrors': ['Нельзя закрыть бронь без указания сотрудника.']})

        reservation.status = new_status.value
        reservation.closed_at = timezone.now()
        reservation.save()
        return reservation

    def prolong_reservation(
        self,
        reservation: WorkReservation,
        *,
        prolong_for_ms: int,
        actor: CustomUser,
    ) -> WorkReservation:
        reservation = cast('WorkReservation', reservation)

        if not WorkReservationStatus(reservation.status).is_open():
            raise ValidationError({'nonFieldErrors': ['Продлить можно только открытую бронь.']})

        if not actor.is_staff_user:
            raise ValidationError({'nonFieldErrors': ['Продлить бронь может только сотрудник.']})

        reservation.reserved_till = reservation.reserved_till + datetime.timedelta(milliseconds=prolong_for_ms)
        reservation.save(update_fields=('reserved_till',))
        return reservation
