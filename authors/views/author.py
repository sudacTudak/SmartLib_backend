from django.db.models import QuerySet
from pydantic import BaseModel, Field
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin, RetrieveModelMixin, \
    UpdateModelMixin
from rest_framework.permissions import SAFE_METHODS

from authors.models import Author
from authors.serializers import AuthorSerializer
from common_core.classes import ViewSetBase
from users.permissions import IsStaff
from typing import cast
from common_core.fields import OptionalListQueryParam

__all__ = ['AuthorViewSet']


class ListQueryParams(BaseModel):
    genres: OptionalListQueryParam[str] = Field(None)
    library_branches: OptionalListQueryParam[str] = Field(None, alias='libraryBranches')

    model_config = {
        'populate_by_name': True
    }


class AuthorViewSet(
    ViewSetBase[QuerySet[Author]],
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsStaff()]

    def get_query_params_model_class(self) -> type[ListQueryParams] | None:
        if self.action == 'list':
            return ListQueryParams
        return None

    def _apply_query_params_for_queryset(self, qs: QuerySet[Author]) -> QuerySet[Author]:
        params = cast(ListQueryParams, self.get_processed_query_params())

        if params is None:
            return qs

        if (genres := params.genres) is not None:
            qs = qs.filter(works__genres__id__in=genres)
        if (branches := params.library_branches) is not None:
            qs = qs.filter(works__work_items__library_branch__id__in=branches)

        return qs
