from http import HTTPMethod

from django.db import transaction
from django.db.models import (
    Avg,
    Case,
    Count,
    ExpressionWrapper,
    F,
    IntegerField,
    OuterRef,
    Q,
    QuerySet,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.viewsets import ReadOnlyModelViewSet

from common_core.classes import ViewSetBase
from http_core import HTTPResponse

from library.models import LibraryBranch
from users.enums import UserPermissions
from users.permissions import HasUserPermission, IsStaff

from typing import cast

from works.models import Work, WorkItem
from works.query_params import WorkListQueryParams, WorkSimilarQueryParams
from works.serializers import WorkSerializer, WorkSimilarSerializer

from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin

__all__ = ['WorkViewSet']

_SIMILAR_WORKS_MIN_SIMILARITY_SCORE = 20


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
        if self.action == 'similar':
            return WorkSimilarQueryParams
        return None

    def get_serializer_class(self):
        if self.action == 'similar':
            return WorkSimilarSerializer
        return WorkSerializer

    def get_queryset(self) -> QuerySet[Work]:
        qs = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            qs = qs.prefetch_related('genres', 'authors').annotate(
                rating_avg=Avg('feedbacks__score'),
                rating_count=Count('feedbacks', distinct=True),
            )
            if self.action in ('list', 'retrieve', 'similar'):
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

    @action(url_path='similar', detail=False, methods=[HTTPMethod.GET])
    def similar(self, request, *args, **kwargs):
        params = cast(WorkSimilarQueryParams, self.get_processed_query_params())
        work_id_str = str(params.work_id)
        source = get_object_or_404(Work.objects.prefetch_related('genres', 'authors'), pk=work_id_str)

        genre_ids = list(source.genres.values_list('pk', flat=True))
        author_ids = list(source.authors.values_list('pk', flat=True))

        qs = self.get_queryset().exclude(pk=work_id_str)

        if genre_ids:
            qs = qs.annotate(
                similar_genres=Count('genres', filter=Q(genres__pk__in=genre_ids), distinct=True),
            )
        else:
            qs = qs.annotate(similar_genres=Value(0, output_field=IntegerField()))

        if author_ids:
            qs = qs.annotate(
                similar_authors=Count(
                    'authors',
                    filter=Q(authors__pk__in=author_ids),
                    distinct=True,
                ),
            )
        else:
            qs = qs.annotate(similar_authors=Value(0, output_field=IntegerField()))

        qs = qs.annotate(
            same_category=Case(
                When(category=source.category, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            ),
        )

        qs = qs.annotate(
            similarity_score=ExpressionWrapper(
                F('similar_genres') * Value(15)
                + F('similar_authors') * Value(12)
                + F('same_category') * Value(8),
                output_field=IntegerField(),
            ),
        ).filter(similarity_score__gte=_SIMILAR_WORKS_MIN_SIMILARITY_SCORE)
        qs = qs.order_by('-similarity_score', 'title')[: params.limit]

        serializer = cast(WorkSimilarSerializer, self.get_serializer(qs, many=True))
        return HTTPResponse.success(data=serializer.data, status_code=status.HTTP_200_OK)

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
