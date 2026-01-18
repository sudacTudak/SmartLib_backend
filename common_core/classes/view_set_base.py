from rest_framework.viewsets import GenericViewSet

from http_core import HTTPResponse
from rest_framework import status

from http_core import ResponseBodyFailure, ResponseBodySuccess

__all__ = ['ViewSetBase']


class ViewSetBase(GenericViewSet):
    object_name: str | None
    _default_name = 'object'

    @property
    def safety_object_name(self):
        return self.object_name if self.object_name is not None else self._default_name

    def make_not_found_response(self, field_id: int, **kwargs):
        message = f'Not found {self.safety_object_name} with id {field_id}'
        return HTTPResponse.failure(status_code=status.HTTP_404_NOT_FOUND,
                                    message=message, **kwargs)

    def make_bad_request_response(self, data=None, **kwargs):
        message = f'Invalid {self.safety_object_name} data provided'
        return HTTPResponse.failure(status_code=status.HTTP_400_BAD_REQUEST, message=message, data=data, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)

        if isinstance(response, HTTPResponse):
            return response

        # Обрабатываем ошибки
        if response.status_code >= 400:
            return response

        body = ResponseBodySuccess(
            status_code=response.status_code,
            data=response.data
        ).get_as_dict()

        response.data = body
        return response
