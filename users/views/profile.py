from http import HTTPMethod

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import TypeCustomUserQuerySet, CustomUser
from typing import cast

from users.serializers import GetUserPublicSerializer, GetStaffSerializer

__all__ = ['ProfileViewSet']

class ProfileViewSet(ViewSetBase[TypeCustomUserQuerySet]):
    queryset: TypeCustomUserQuerySet = CustomUser.objects.all()
    serializer_class = GetUserPublicSerializer

    def get_permissions(self):
        return [IsAuthenticated(),]

    @action(url_path='', url_name='profile', detail=False, methods=[HTTPMethod.GET])
    def profile(self):
        user = cast(CustomUser, self.request.user)

        if user.is_staff_user:
            serializer = cast(GetStaffSerializer, self.get_serializer(user))
        else:
            serializer = cast(GetUserPublicSerializer, self.get_serializer(user))

        serializer.is_valid(raise_exception=True)

        return HTTPResponse.success(data=serializer.validated_data, status_code=status.HTTP_200_OK)
