from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from library.models import LibraryBranch
from positions.models import StaffPosition
from users.models import CustomUser
from users.validators import AppPasswordValidator

__all__ = ['CreateStaffSerializer']


class CreateStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=6, write_only=True, required=True,
                                     validators=[AppPasswordValidator])
    library_branch_id = PrimaryKeyRelatedField(queryset=LibraryBranch.objects.all(),
                                               source='staff_profile.library_branch')
    position_id = PrimaryKeyRelatedField(queryset=StaffPosition.objects.all(), source='staff_profile.position')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'password', 'last_name', 'patronymic', 'gender', 'role', 'library_branch_id',
                  'position_id')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        print('validated_data: ', validated_data)
        staff_profile = validated_data.pop('staff_profile')
        profile_data = dict(library_branch=staff_profile.pop('library_branch'),
                            position=staff_profile.pop('position'))

        return CustomUser.objects.create_staff(profile_data=profile_data, **validated_data)
