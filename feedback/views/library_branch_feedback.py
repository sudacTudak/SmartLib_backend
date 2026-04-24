from http import HTTPMethod
from typing import cast

from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from common_core.classes import ViewSetBase
from feedback.models import LibraryBranchFeedback
from feedback.permissions import IsStaffOrFeedbackOwner
from feedback.query_params import LibraryBranchByUserQueryParams
from feedback.serializers import LibraryBranchFeedbackSerializer
from http_core import HTTPResponse
from users.permissions import IsStaff

__all__ = ['LibraryBranchFeedbackViewSet']


class LibraryBranchFeedbackViewSet(
    ViewSetBase[QuerySet[LibraryBranchFeedback]],
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = LibraryBranchFeedbackSerializer

    def get_query_params_model_class(self):
        if self.action in ('list', 'by_user'):
            return LibraryBranchByUserQueryParams
        return None

    def get_permissions(self):
        if self.action in ('list',):
            return [IsStaff()]

        if self.action in ('by_user', 'create'):
            return [IsAuthenticated()]

        if self.action in ('partial_update', 'destroy'):
            return [IsAuthenticated(), IsStaffOrFeedbackOwner()]

        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet[LibraryBranchFeedback]:
        if self.action in ('list', 'by_user'):
            params = cast(LibraryBranchByUserQueryParams | None, self.get_processed_query_params())
            qs = LibraryBranchFeedback.objects.all().select_related('library_branch', 'client')
            if params is not None and params.library_branch_id is not None:
                qs = qs.filter(library_branch_id=str(params.library_branch_id))
            return qs

        if self.action in ('create', 'partial_update', 'destroy'):
            return LibraryBranchFeedback.objects.all().select_related('library_branch', 'client')

        return LibraryBranchFeedback.objects.none()

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError as exc:
            raise ValidationError({'nonFieldErrors': ['Отзыв для этого филиала уже существует']}) from exc

    @action(detail=False, methods=[HTTPMethod.GET], url_path='by-user')
    def by_user(self, request: Request, *_args, **_kwargs):
        qs = self.get_queryset()
        if IsStaff().has_permission(request, self):
            client_id = request.query_params.get('client_id') or request.query_params.get('clientId')
            if not client_id:
                return HTTPResponse.failure(
                    message='Укажите client_id',
                    status_code=status.HTTP_400_BAD_REQUEST,
                )
            qs = qs.filter(client_id=client_id)
        else:
            qs = qs.filter(client_id=request.user.id)

        serializer = self.get_serializer(qs, many=True)
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)
