from http import HTTPMethod

from django.http import Http404
from pydantic import BaseModel, Field, UUID4
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin

from common_core.classes import ViewSetBase
from http_core import HTTPResponse
from users.models import CustomUser, CustomUserQuerySet, UserPermission
from users.permissions import IsStaff, HasUserPermission, CanModifyPermissions, SameLibraryObjectPermission
from users.serializers import GetStaffSerializer, UpdateUserPermissionSerializer, CreateStaffSerializer, UpdateStaffSerializer
from typing import cast
from users.enums import UserPermissions, UserRole

from common_core.fields import OptionalListQueryParam

__all__ = ['StaffViewSet', 'StaffListQueryParams']


class StaffListQueryParams(BaseModel):
    library_id: UUID4 | None = Field(None, alias='libraryId')
    position_id: UUID4 | None = Field(None, alias='positionId')
    email: str | None = Field(None)
    permissions: OptionalListQueryParam[UserPermissions] = None

    model_config = {
        "populate_by_name": True
    }


class StaffViewSet(
    ViewSetBase[CustomUserQuerySet],
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = CustomUser.objects.all()

    def get_query_params_model_class(self):
        if self.action == 'list':
            return StaffListQueryParams
        return None

    def _get_base_model_queryset(self) -> CustomUserQuerySet:
        user = cast(CustomUser, self.request.user)
        if not user.is_authenticated:
            raise NotAuthenticated(
                f'Невозможно получить доступ к данным {self.basename}: пользователь не авторизован.'
            )
        return CustomUser.objects.all().scoped_for_staff_same_library(user)

    def _apply_query_params_for_queryset(self, qs: CustomUserQuerySet) -> CustomUserQuerySet:
        params = cast(StaffListQueryParams | None, self.get_processed_query_params())
        if params is None:
            return qs
        result_qs = qs

        if library_id := params.library_id:
            user = cast(CustomUser, self.request.user)

            if user.is_admin:
                result_qs = result_qs.get_library_managers(str(library_id))

        if position_id := params.position_id:
            result_qs = result_qs.filter(staff_profile__position=position_id)
        if email := params.email:
            result_qs = result_qs.filter(email__icontains=email)
        if permissions := params.permissions:
            result_qs = result_qs.filter(user_permissions__code__in=[perm.value for perm in permissions])

        return result_qs

    def get_permissions(self):
        if self.action == 'update_permissions':
            return [IsStaff(), CanModifyPermissions()]

        if self.action == 'create':
            return [IsStaff(), HasUserPermission(UserPermissions.ManagerAdministration)]

        if self.action in ('partial_update', 'destroy'):
            return [
                IsStaff(),
                SameLibraryObjectPermission(object_library_branch_lookup='staff_profile__library_branch_id'),
            ]

        return [IsStaff()]

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            return CreateStaffSerializer(*args, **kwargs)

        if self.action == 'partial_update':
            return UpdateStaffSerializer(*args, **kwargs)

        return GetStaffSerializer(*args, **kwargs)

    @action(url_path='update-permissions', detail=True, methods=(HTTPMethod.PATCH,))
    def update_permissions(self, request, *args, **kwargs):
        user_id = kwargs.get(self.lookup_field, None)

        try:
            user = cast(CustomUser, self.get_object())
        except Http404:
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
