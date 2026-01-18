from rest_framework.response import Response
from rest_framework import status

from http_core import ResponseBodySuccess, ResponseBodyFailure

__all__ = ['HTTPResponse']


class HTTPResponse(Response):
    def __init__(self, status_code: int = status.HTTP_200_OK, data=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        super().__init__(data, status=status_code, template_name=template_name, headers=headers, exception=exception,
                         content_type=content_type)

    @classmethod
    def success(cls, status_code: int = status.HTTP_200_OK, data=None, template_name=None, headers=None,
                exception=False, content_type=None):
        response_body = ResponseBodySuccess(status_code, data).get_as_dict()
        return cls(status_code, response_body, template_name, headers, exception, content_type)

    @classmethod
    def failure(cls, status_code: int = status.HTTP_400_BAD_REQUEST, message: str = '', data=None, template_name=None,
                headers=None, exception=False, content_type=None):
        response_body = ResponseBodyFailure(status_code, message, data).get_as_dict()
        return cls(status_code, response_body, template_name, headers, exception, content_type)