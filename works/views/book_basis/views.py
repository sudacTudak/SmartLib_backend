from django.db.models import Avg, Count, IntegerField, OuterRef, QuerySet, Subquery, Sum
from django.db.models.functions import Coalesce
from rest_framework import status
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

from works.models import Work, WorkItem
from common_core.classes import ViewSetBase
from http_core import HTTPResponse

from works.serializers import WorkSerializer
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from django.db import transaction
from typing import cast

from works.query_params import WorkListQueryParams
from library.models import LibraryBranch

from users.permissions import HasUserPermission, IsStaff
from users.enums import UserPermissions

__all__ = ['WorkViewSet']


class WorkViewSet(
    ViewSetBase[QuerySet[Work]],
    ReadOnlyModelViewSet,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    serializer_class = WorkSerializer
    queryset = Work.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return WorkListQueryParams
        return None

    def get_queryset(self) -> QuerySet[Work]:
        qs = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            qs = qs.prefetch_related('genres', 'authors').annotate(
                rating_avg=Avg('feedbacks__score'),
                rating_count=Count('feedbacks', distinct=True),
            )
            if self.action in ('list', 'retrieve'):
                books_available_subq = (
                    WorkItem.objects.filter(work_id=OuterRef('pk'))
                    .values('work_id')
                    .annotate(_avail_sum=Sum('available_count'))
                    .values('_avail_sum')[:1]
                )
                qs = qs.annotate(
                    books_available_total=Coalesce(
                        Subquery(books_available_subq, output_field=IntegerField()),
                        0,
                    ),
                )
            if self.action == 'list':
                params = cast(WorkListQueryParams | None, self.get_processed_query_params())
                if params is not None and params.only_available is True:
                    qs = qs.filter(books_available_total__gt=0)
                if params is not None and params.category is not None:
                    qs = qs.filter(category=str(params.category))
        return qs

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        if self.action == 'partial_update':
            return [IsStaff(), HasUserPermission(UserPermissions.BookBasesModification)]
        return [IsStaff(), HasUserPermission(UserPermissions.UsersAdministration)]

    def destroy(self, request, *args, **kwargs):
        work = self.get_object()
        serializer = self.get_serializer(work)
        response_data = serializer.data
        self.perform_destroy(work)
        return HTTPResponse.success(data=response_data, status_code=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer = cast(WorkSerializer, serializer)

        with transaction.atomic():
            work = cast(Work, serializer.save())
            library_branches_qs = LibraryBranch.objects.all()

            WorkItem.objects.bulk_create(
                WorkItem(work=work, library_branch=branch, total_count=0, available_count=0)
                for branch in library_branches_qs
            )

