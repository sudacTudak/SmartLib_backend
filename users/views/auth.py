from http import HTTPMethod
from tokenize import TokenError

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status
from rest_framework_simplejwt.exceptions import ExpiredTokenError
from rest_framework_simplejwt.tokens import RefreshToken

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import CustomUser, CustomUserQuerySet
from users.serializers import RegisterUserSerializer, ChangePasswordSerializer, LogoutSerializer, LoginSerializer

__all__ = ['AuthViewSet']


class AuthViewSet(ViewSetBase[CustomUserQuerySet]):
    queryset = CustomUser.objects.all()

    def get_serializer_class(self):
        if self.action == 'change_password':
            return ChangePasswordSerializer
        if self.action == 'register':
            return RegisterUserSerializer
        if self.action == 'logout':
            return LogoutSerializer
        return LoginSerializer

    # Этот метод не должен использоваться при создании менеджера/админа -
    # обрабатывать нужно отдельно, будто менеджер/админ создает другого менеджера/админа
    @action(url_path='register', detail=False, methods=[HTTPMethod.POST])
    def register(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return HTTPResponse.success(status_code=status.HTTP_201_CREATED)

    @action(url_path='login', detail=False, methods=['POST'])
    def login(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = CustomUser.objects.get_by_email(email)
        print('user: ', user)
        print('user check password: ', user.check_password(password))
        if not user or not user.check_password(password):
            return HTTPResponse.failure(message="Неверный email или пароль", status_code=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return HTTPResponse.success(data={
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status_code=status.HTTP_200_OK)

    @action(url_path='logout', detail=False, methods=[HTTPMethod.POST])
    def logout(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data.get('refresh')

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except (TokenError, ExpiredTokenError) as e:
            return HTTPResponse.failure(message=e, status_code=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return HTTPResponse.failure(message='Некорректный refresh_token', status_code=status.HTTP_400_BAD_REQUEST)

        return HTTPResponse.success(status_code=status.HTTP_205_RESET_CONTENT)


    @action(url_path='change-password', detail=True, methods=[HTTPMethod.POST])
    def change_password(self, request: Request, *_args, **_kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return HTTPResponse.success(status_code=status.HTTP_200_OK)
