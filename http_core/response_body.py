import abc

__all__ = ['ResponseBodyBase', 'ResponseBodySuccess', 'ResponseBodyFailure']


class ResponseBodyBase(abc.ABC):

    def __init__(self, status_code):
        self.status_code = status_code

    def get_as_dict(self):
        return {
            'status_code': self.status_code
        }


class ResponseBodySuccess(ResponseBodyBase):
    def __init__(self, status_code, data):
        super().__init__(status_code)
        self.data = data

    def get_as_dict(self):
        base_response = super().get_as_dict()
        return {
            **base_response,
            'data': self.data,
        }


class ResponseBodyFailure(ResponseBodyBase):
    def __init__(self, status_code, message, data=None):
        super().__init__(status_code)
        self.message = message
        self.data = data

    def get_as_dict(self):
        response_body = {
            **super().get_as_dict(),
            "message": self.message
        }

        if self.data is not None:
            response_body['data'] = self.data

        return response_body
