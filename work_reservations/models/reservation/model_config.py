from __future__ import annotations

import datetime

from django.core.exceptions import ValidationError

__all__ = [
    'WorkReservationModelConfig',
    'get_reserved_till_min_date',
    'get_reserved_till_max_date',
    'reserved_till_validator',
]


class WorkReservationModelConfig:
    MIN_UNIQUE_INDEX = 100_000_000
    MAX_UNIQUE_INDEX = 999_999_999
    MIN_RESERVED_TILL_OFFSET_DAYS = 1
    MAX_RESERVED_TILL_OFFSET_WEEKS = 2


def get_reserved_till_min_date() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(days=WorkReservationModelConfig.MIN_RESERVED_TILL_OFFSET_DAYS)


def get_reserved_till_max_date() -> datetime.date:
    return datetime.date.today() + datetime.timedelta(weeks=WorkReservationModelConfig.MAX_RESERVED_TILL_OFFSET_WEEKS)


def reserved_till_validator(value: datetime.date) -> None:
    min_date = get_reserved_till_min_date()
    max_date = get_reserved_till_max_date()

    if value < min_date:
        raise ValidationError(
            f'Дата брони не может быть раньше {min_date.isoformat()} (минимум +1 день от сегодня).',
            code='reserved_till_min',
        )
    if value > max_date:
        raise ValidationError(
            f'Дата брони не может быть позже {max_date.isoformat()} (максимум +2 недели от сегодня).',
            code='reserved_till_max',
        )
