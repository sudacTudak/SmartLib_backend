from __future__ import annotations

from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError
from uuid import uuid4 as uuid

from library.models import LibraryBranch
from users.models import CustomUser
from work_reservations.enums import WorkReservationStatus
from work_reservations.models.reservation.manager import WorkReservationManager
from work_reservations.models.reservation.model_config import (
    WorkReservationModelConfig,
    reserved_till_validator,
)
from works.models import Work

__all__ = ['WorkReservation']

index_validators = [
    MinValueValidator(WorkReservationModelConfig.MIN_UNIQUE_INDEX),
    MaxValueValidator(WorkReservationModelConfig.MAX_UNIQUE_INDEX),
]

reserved_till_validators = [reserved_till_validator]


class WorkReservation(models.Model):
    id: str = models.UUIDField(primary_key=True, editable=False, default=uuid)
    index: int = models.PositiveIntegerField(validators=index_validators)
    client: CustomUser = models.ForeignKey(
        CustomUser,
        related_name='work_reservations_client',
        on_delete=models.PROTECT,
    )
    client_id: str

    work: Work = models.ForeignKey(Work, related_name='reservations', on_delete=models.PROTECT)
    work_id: str

    library_branch: LibraryBranch = models.ForeignKey(
        LibraryBranch,
        related_name='work_reservations',
        on_delete=models.PROTECT,
    )
    library_branch_id: str

    status: int = models.PositiveIntegerField(
        choices=WorkReservationStatus.as_django_model_choices(),
        default=WorkReservationStatus.Open.value,
    )

    responsible_staff: CustomUser | None = models.ForeignKey(
        CustomUser,
        related_name='work_reservations_staff',
        on_delete=models.PROTECT,
        null=True,
    )
    responsible_staff_id: str | None

    created_at = models.DateTimeField(auto_now_add=True)
    reserved_till = models.DateField(null=False, blank=False, validators=reserved_till_validators)
    closed_at = models.DateTimeField(null=True)

    objects = WorkReservationManager()

    class Meta:
        db_table = 'work_reservation'
        ordering = ('created_at', 'status', 'reserved_till',)

    def __str__(self):
        return f'{self.id}_{WorkReservationStatus(self.status).name}'

    def save(self, *args, **kwargs):
        if not self.pk and not WorkReservationStatus(self.status).is_open():
            raise ValidationError(
                f'Reservation should have only {WorkReservationStatus.Open} status for creation. Current is {WorkReservationStatus(self.status)}',
            )

        try:
            self.full_clean()
        except DjangoValidationError as exc:
            raise ValidationError(exc.message_dict or exc.messages) from exc

        super().save(*args, **kwargs)
