from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from http_core import HTTPResponse

from http_core import ResponseBodyFailure, ResponseBodySuccess
from typing import Generic, TypeVar, cast

__all__ = ['ViewSetBase']

ModelT = TypeVar("ModelT")


class ViewSetBase(Generic[ModelT], GenericViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self) -> QuerySet[ModelT]:
        return super().get_queryset()

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
