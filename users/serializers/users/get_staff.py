from rest_framework import  serializers
from rest_framework.relations import PrimaryKeyRelatedField

from users.models import CustomUser

__all__ = ['GetStaffSerializer']


class GetStaffSerializer(serializers.ModelSerializer):
    # user_permissions = PrimaryKeyRelatedField(many=True, read_only=True)
    library_branch_id = PrimaryKeyRelatedField(source='staff_profile.library_branch')
    position_id = PrimaryKeyRelatedField(source='staff_profile.position')

    class Meta:
        model = CustomUser
        exclude = ('password',)