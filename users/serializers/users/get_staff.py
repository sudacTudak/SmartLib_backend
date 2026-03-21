from rest_framework import serializers

from users.models import CustomUser
from users.serializers.permissions import ReadUserPermissionsSerializer

__all__ = ['GetStaffSerializer']



class GetStaffSerializer(serializers.ModelSerializer):
    library_branch_id = serializers.UUIDField(
        source="staff_profile.library_branch_id",
        read_only=True,
        allow_null=True
    )
    position_id = serializers.UUIDField(
        source="staff_profile.position_id",
        read_only=True,
        allow_null=True
    )
    user_permissions = ReadUserPermissionsSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ("id",
                  "email",
                  "first_name",
                  "last_name",
                  "patronymic",
                  "gender",
                  "role",
                  "library_branch_id",
                  "position_id",
                  "user_permissions",)
