from http import HTTPMethod

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import CustomUser
from users.serializers import RegisterUserSerializer, ChangePasswordSerializer

__all__ = ['AuthViewSet']


class AuthViewSet(ViewSetBase[CustomUser]):
    queryset = CustomUser.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'change_password':
            return ChangePasswordSerializer(*args, **kwargs)

        return RegisterUserSerializer(*args, **kwargs)

    # Этот метод не должен использоваться при создании менеджера/админа -
    # обрабатывать нужно отдельно, будто менеджер/админ создает другого менеджера/админа
    @action(url_path='register', detail=False, methods=[HTTPMethod.POST])
    def register(self, request: Request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return HTTPResponse.success(status_code=status.HTTP_201_CREATED)

    @action(url_path='change-password', detail=True, methods=[HTTPMethod.POST])
    def change_password(self, request: Request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return HTTPResponse.success(status_code=status.HTTP_200_OK)
