from __future__ import annotations

from http import HTTPMethod
from typing import cast

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import CustomUser
from users.permissions import SameLibraryObjectPermission
from work_reservations.enums import WorkReservationStatus
from work_reservations.models import WorkReservation
from work_reservations.models.reservation.queryset import WorkReservationQuerySet
from work_reservations.permissions import CanManageWorkReservations, IsClient, IsStaffOrReservationClient
from work_reservations.query_params import WorkReservationListQueryParams
from work_reservations.serializer import (
    ClientReadWorkReservationSerializer,
    StaffReadWorkReservationSerializer,
    WorkReservationProlongSerializer,
    WorkReservationStatusSerializer,
    WriteWorkReservationSerializer,
)

__all__ = ['WorkReservationViewSet']


class WorkReservationViewSet(
    ViewSetBase[WorkReservationQuerySet],
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
):
    queryset = WorkReservation.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return WorkReservationListQueryParams
        return None

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'status'):
            return [IsAuthenticated()]

        if self.action == 'prolong':
            return [IsAuthenticated(), CanManageWorkReservations()]

        if self.action == 'create':
            return [IsAuthenticated(), IsClient()]

        return [IsAuthenticated()]

    def _get_base_model_queryset(self) -> WorkReservationQuerySet:
        user = cast(CustomUser, self.request.user)
        qs = cast(WorkReservationQuerySet, super()._get_base_model_queryset())

        if user.is_staff_user:
            return qs.scoped_for_staff_same_library(user)
        return qs.filter(client_id=user.id)

    def _apply_query_params_for_queryset(self, qs: WorkReservationQuerySet) -> WorkReservationQuerySet:
        params = cast(WorkReservationListQueryParams | None, self.get_processed_query_params())
        if params is None:
            return qs

        user = cast(CustomUser, self.request.user)

        if params.client_id is not None:
            if not user.is_staff_user and str(params.client_id) != str(user.id):
                return qs.none()
            qs = qs.filter(client_id=str(params.client_id))

        if params.status is not None:
            qs = qs.filter(status=params.status.value)

        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return WriteWorkReservationSerializer
        if self.action == 'status':
            return WorkReservationStatusSerializer
        if self.action == 'prolong':
            return WorkReservationProlongSerializer
        if self.action in ('retrieve', 'list'):
            user = cast(CustomUser, self.request.user)
            if user.is_staff_user:
                return StaffReadWorkReservationSerializer
            return ClientReadWorkReservationSerializer
        return ClientReadWorkReservationSerializer

    def get_read_serializer(self, instance: WorkReservation):
        user = cast(CustomUser, self.request.user)
        serializer_class = (
            StaffReadWorkReservationSerializer
            if user.is_staff_user
            else ClientReadWorkReservationSerializer
        )
        return serializer_class(instance, context=self.get_serializer_context())

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        user = cast(CustomUser, request.user)

        if self.action == 'retrieve':
            if not IsStaffOrReservationClient().has_object_permission(request, self, obj):
                self.permission_denied(request)

        if self.action == 'status':
            if user.is_staff_user:
                if user.is_manager:
                    if not CanManageWorkReservations().has_permission(request, self):
                        self.permission_denied(request)
                    if not SameLibraryObjectPermission(
                        object_library_branch_lookup='library_branch_id',
                    ).has_object_permission(request, self, obj):
                        self.permission_denied(request)
            elif str(obj.client_id) != str(user.id):
                self.permission_denied(request)

        if self.action == 'prolong':
            if not SameLibraryObjectPermission(
                object_library_branch_lookup='library_branch_id',
            ).has_object_permission(request, self, obj):
                self.permission_denied(request)

    def create(self, request: Request, *args, **kwargs):
        user = cast(CustomUser, request.user)
        data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
        data['clientId'] = str(user.id)

        serializer = cast(WriteWorkReservationSerializer, self.get_serializer(data=data))
        serializer.is_valid(raise_exception=True)
        reservation = cast(WorkReservation, serializer.save())
        response_serializer = self.get_read_serializer(reservation)
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_201_CREATED)

    @action(url_path='status', detail=True, methods=(HTTPMethod.PATCH,))
    def status(self, request: Request, *args, **kwargs):
        reservation = cast(WorkReservation, self.get_object())
        serializer = cast(WorkReservationStatusSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)

        user = cast(CustomUser, request.user)
        new_status = WorkReservationStatus(serializer.validated_data['status'])

        if user.is_staff_user:
            if new_status not in (WorkReservationStatus.Closed, WorkReservationStatus.StaffDeclined):
                raise PermissionDenied('Сотрудник может установить только статус Closed или StaffDeclined.')
        elif new_status != WorkReservationStatus.ClientDeclined:
            raise PermissionDenied('Клиент может установить только статус ClientDeclined.')

        reservation = WorkReservation.objects.change_status(
            reservation,
            new_status=new_status,
            actor=user,
        )

        response_serializer = self.get_read_serializer(reservation)
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_200_OK)

    @action(url_path='prolong', detail=True, methods=(HTTPMethod.PATCH,))
    def prolong(self, request: Request, *args, **kwargs):
        reservation = cast(WorkReservation, self.get_object())
        serializer = cast(WorkReservationProlongSerializer, self.get_serializer(data=request.data))
        serializer.is_valid(raise_exception=True)

        user = cast(CustomUser, request.user)
        prolong_time_ms = cast(int, serializer.validated_data['prolong_time'])
        reservation = WorkReservation.objects.prolong_reservation(
            reservation,
            prolong_for_ms=prolong_time_ms,
            actor=user,
        )

        response_serializer = self.get_read_serializer(reservation)
        return HTTPResponse.success(data=response_serializer.data, status_code=status.HTTP_200_OK)
