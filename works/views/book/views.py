from http import HTTPMethod

from typing import cast

from django.db.models import QuerySet, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import get_object_or_404
from pydantic import BaseModel
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.request import Request

from common_core.classes.view_set_base import QuerySetT
from works.models import WorkItem
from works.serializers import WorkItemByLibrarySerializer
from common_core.classes import ViewSetBase
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import ParseError

from http_core import HTTPResponse
from library.models import LibraryBranch

__all__ = ['WorkItemViewSet']

from works.views.book.query_params import AvailabilityInfoByWorkQueryParams, ListByWorkQueryParams


class WorkItemViewSet(ViewSetBase[QuerySet[WorkItem]], RetrieveModelMixin):
    serializer_class = WorkItemByLibrarySerializer
    queryset = WorkItem.objects.all()

    def get_queryset(self) -> QuerySet[WorkItem]:
        qs = super().get_queryset()

        if self.request.method in SAFE_METHODS:
            qs = qs.select_related('work').prefetch_related('work__genres', 'work__authors')

        return qs

    def get_query_params_model_class(self) -> type[BaseModel] | None:
        if self.action == 'by_work':
            return ListByWorkQueryParams

        if self.action == 'availability_by_work':
            return AvailabilityInfoByWorkQueryParams

        return None

    def _apply_query_params_for_queryset(self, qs: QuerySetT) -> QuerySet[WorkItem]:
        return qs

    @action(url_path='by-library', detail=False, methods=[HTTPMethod.GET])
    def list_by_library_branch(self, request: Request, *_args, **_kwargs):
        filter_params: dict[str, str | bool] = {}

        if (library_branch_id := request.query_params.get('library')) is None:
            raise ParseError(detail='Library branch id is not provided')

        filter_params['library_branch_id'] = str(library_branch_id)

        get_object_or_404(LibraryBranch, pk=library_branch_id)

        if title := request.query_params.get('title'):
            filter_params['work__title__icontains'] = str(title)

        queryset = self.get_queryset().filter(**filter_params)
        serializer = cast(WorkItemByLibrarySerializer, self.get_serializer(queryset, many=True))

        return HTTPResponse.success(data=serializer.data, status_code=200)

    @action(url_path='by-work', detail=False, methods=[HTTPMethod.GET])
    def list_by_work(self, request: Request, *_args, **_kwargs):
        if (work_id := request.query_params.get('work') or request.query_params.get('workId')) is None:
            raise ParseError(detail='Work id is not provided')

        qs = self.get_queryset().filter(work_id=str(work_id))

        only_available = request.query_params.get('only_available') or request.query_params.get('onlyAvailable')
        if str(only_available).lower() in ('1', 'true', 'yes'):
            qs = qs.filter(available_count__gt=0)

        serializer = cast(WorkItemByLibrarySerializer, self.get_serializer(qs, many=True))
        return HTTPResponse.success(data=serializer.data, status_code=200)

    @action(url_path='availability-by-work', detail=False, methods=[HTTPMethod.GET])
    def availability_by_work(self, request: Request, *_args, **_kwargs):
        params = cast(AvailabilityInfoByWorkQueryParams | None, self.get_processed_query_params())
        print('params: ', params)
        if params is None or params.work_id is None:
            return HTTPResponse.failure(
                message='Не указан идентификатор произведения (workId)',
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        work_id = str(params.work_id)

        items_for_work = WorkItem.objects.filter(work_id=work_id)
        if not items_for_work.exists():
            return HTTPResponse.failure(
                message='Для этого произведения нет записей экземпляров (WorkItem)',
                status_code=status.HTTP_404_NOT_FOUND,
            )

        item_qs = items_for_work.filter(available_count__gt=0)

        total_available_count = item_qs.aggregate(
            total=Coalesce(Sum('available_count'), 0),
        )['total']

        available_by_library_branch_ids = {
            str(branch_id): int(avail)
            for branch_id, avail in item_qs.values_list('library_branch_id', 'available_count')
        }

        return HTTPResponse.success(
            data={
                'work_id': work_id,
                'total_available_count': int(total_available_count),
                'available_by_library_branch_ids': available_by_library_branch_ids,
            },
            status_code=200,
        )
