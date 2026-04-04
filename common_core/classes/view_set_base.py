from django.db.models import QuerySet
from pydantic import BaseModel, ValidationError
from rest_framework.exceptions import ParseError
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from http_core import HTTPResponse

from http_core import ResponseBodySuccess
from typing import Any, Generic, TypeVar, cast

__all__ = ['ViewSetBase']

QuerySetT = TypeVar("QuerySetT", bound=QuerySet[Any])


class ViewSetBase(Generic[QuerySetT], GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    _processed_query_params: BaseModel | None = None

    def initial(self, request: Request, *args, **kwargs):
        self._parse_and_cache_query_params(request.query_params)
        super().initial(request, *args, **kwargs)

    def get_query_params_model_class(self) -> type[BaseModel] | None:
        """Подкласс возвращает pydantic-модель для текущего action или None (парсинг не нужен)."""
        return None

    def get_processed_query_params(self) -> BaseModel | None:
        """Экземпляр pydantic-модели после model_validate; None если модель для action не задана."""
        return self._processed_query_params

    def _parse_and_cache_query_params(self, query_params: dict[str, str]) -> None:
        if (model_cls := self.get_query_params_model_class()) is None:
            self._processed_query_params = None
            return
        try:
            self._processed_query_params = model_cls.model_validate(query_params)
        except ValidationError as exc:
            raise ParseError(detail=exc.errors())

    def _get_base_model_queryset(self) -> QuerySetT:
        return super().get_queryset()

    def _apply_query_params_for_queryset(self, qs: QuerySetT) -> QuerySetT:
        if self.get_processed_query_params() is None:
            return qs
        return qs

    def get_queryset(self) -> QuerySetT:
        qs = self._get_base_model_queryset()
        qs = self._apply_query_params_for_queryset(qs)

        return qs

    def get_raw_query_params(self) -> dict[str, str]:
        return cast(Request, cast(object, self.request)).query_params

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if isinstance(response, HTTPResponse):
            return response

        # Ошибки уже в нужном формате после обработки exception_handler
        if response.status_code >= 400:
            return response

        body = ResponseBodySuccess(
            status_code=response.status_code,
            data=response.data
        ).get_as_dict()

        response.data = body
        return response
