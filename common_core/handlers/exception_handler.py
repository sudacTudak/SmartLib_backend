from rest_framework.views import exception_handler
from rest_framework.exceptions import NotFound, ValidationError
from http_core import ResponseBodyFailure

__all__ = ['custom_exception_handler']


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return response

    if isinstance(exc, NotFound):
        message = str(exc)
    elif isinstance(exc, ValidationError):
        message = 'Validation failed'
    else:
        message = 'Request failed'

    response.data = ResponseBodyFailure(
        status_code=response.status_code,
        message=message,
        data=response.data
    ).get_as_dict()

    return response
