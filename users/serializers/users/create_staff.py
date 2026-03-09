from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from library.models import LibraryBranch
from positions.models import Position
from users.models import CustomUser
from users.validators import AppPasswordValidator

__all__ = ['CreateStaffSerializer']


class CreateStaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=6, write_only=True, required=True,
                                     validators=[AppPasswordValidator])
    library_branch_id = PrimaryKeyRelatedField(queryset=LibraryBranch.objects.all())
    position_id = PrimaryKeyRelatedField(queryset=Position.objects.all())

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'password', 'last_name', 'patronymic', 'gender', 'role', 'staff_profile')

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        profile_data = dict(library_branch = validated_data.pop('library_branch_id'), position = validated_data.pop('position_id'))

        return CustomUser.objects.create_superuser(profile_data=profile_data, **validated_data)
