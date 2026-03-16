from rest_framework import serializers

from users.enums import UserPermissions

__all__ = ['UpdateUserPermissionSerializer']


class UpdateUserPermissionSerializer(serializers.Serializer):
    permissions = serializers.MultipleChoiceField(
        choices=UserPermissions.as_django_serializer_choices(),
        required=True,
    )