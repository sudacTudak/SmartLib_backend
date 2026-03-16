from http import HTTPMethod

from django.http import Http404
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework import status

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import CustomUser, CustomUserQuerySet, UserPermission
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin

from users.permissions import IsStaff, HasUserPermission, CanModifyPermissions
from users.serializers import GetStaffSerializer, UpdateUserPermissionSerializer, CreateStaffSerializer
from typing import cast
from users.enums import UserPermissions, UserRole

__all__ = ['StaffViewSet']


class StaffViewSet(ViewSetBase[CustomUser], RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    queryset = CustomUser.objects.all()

    def get_queryset(self) -> CustomUserQuerySet:
        return CustomUser.objects.get_staff()

    def get_permissions(self):
        if self.action == 'update_permissions':
            return [IsStaff(), CanModifyPermissions()]

        if self.action == 'create':
            return [IsStaff(), HasUserPermission(UserPermissions.ManagerAdministration)]

        return [IsStaff()]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return CreateStaffSerializer(*args, **kwargs)

        return GetStaffSerializer(*args, **kwargs)

    @action(url_path='by-library', detail=False, methods=(HTTPMethod.GET,))
    def by_library(self, request: Request, *args, **kwargs):
        print(f'{self.__class__.__name__} by_library method not implemented')
        pass

    @action(url_path='update-permissions', detail=True, methods=(HTTPMethod.PATCH,))
    def update_permissions(self, request, *args, **kwargs):
        user_id = kwargs.get(self.lookup_field, None)

        try:
            user = cast(CustomUser, self.get_object())
        except (Http404,) as e:
            print(e)
            raise Http404(f'Пользователь с идентификатором {user_id} не найден')

        serializer = UpdateUserPermissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        codes = serializer.validated_data.get('permissions')

        if user.role != UserRole.Admin:
            for code in codes:
                if (permission := UserPermissions(code)) in CustomUser.admin_only_permissions:
                    return HTTPResponse.failure(status_code=status.HTTP_400_BAD_REQUEST,
                                                message=f'Доступ <{permission.name}:{permission.value}> может быть только у администратора')

        permissions_qs = UserPermission.objects.filter(code__in=codes)
        user.user_permissions.set(permissions_qs)

        user_serializer = self.get_serializer(user)

        return HTTPResponse.success(data=user_serializer.data, status_code=status.HTTP_200_OK)
