from typing import cast

from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny

from common_core.classes import ViewSetBase
from common_core.classes.view_set_base import QuerySetT
from feedback.models import WorkFeedback
from feedback.permissions import IsStaffOrFeedbackOwner
from feedback.query_params import WorkFeedbackListQueryParams
from feedback.serializers import WorkFeedbackSerializer
from http_core import HTTPResponse
from users.permissions import IsStaff

__all__ = ['WorkFeedbackViewSet']


class WorkFeedbackViewSet(
    ViewSetBase[QuerySet[WorkFeedback]],
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = WorkFeedbackSerializer
    queryset = WorkFeedback.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return WorkFeedbackListQueryParams
        return None

    def get_permissions(self):
        if self.action in ('partial_update', 'destroy'):
            return [IsAuthenticated(), IsStaffOrFeedbackOwner()]

        if self.action in ('create',):
            return [IsAuthenticated()]

        return [AllowAny()]

    def _apply_query_params_for_queryset(self, qs: QuerySetT) -> QuerySetT:
        if self.action == 'list':
            params = cast(WorkFeedbackListQueryParams, self.get_processed_query_params())

            if params is None:
                return qs

            if (work_id := params.work_id) is not None:
                qs = qs.filter(work_id=work_id)
            if (client_id := params.client_id) is not None:
                if not IsStaff().has_permission():
                    if self.request.user.id != client_id:
                        return HTTPResponse.failure(
                            message='Запрещен запрос чужих отзывов',
                            status_code=status.HTTP_400_BAD_REQUEST,
                        )
                qs = qs.filter(client_id=client_id)

        return qs

    def get_queryset(self) -> QuerySet[WorkFeedback]:
        qs = cast(QuerySet[WorkFeedback], super().get_queryset())

        if self.action in ('list',):
            return qs.all().select_related('work', 'client')

        return qs

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            raise ValidationError({'nonFieldErrors': ['Отзыв для этой книги уже существует']}) from exc
