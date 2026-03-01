from rest_framework import  serializers
from rest_framework.relations import PrimaryKeyRelatedField

from users.models import CustomUser, UserPermission


class GetStaffUserSerializer(serializers.ModelSerializer):
    user_permissions = PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CustomUser
        exclude = ('password',)