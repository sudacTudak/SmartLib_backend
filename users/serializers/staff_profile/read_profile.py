from rest_framework import serializers
from users.models import StaffProfile

__all__ = ['ReadStaffProfileSerializer']

class ReadStaffProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProfile
        fields = ['library_branch', 'user', 'position']
        read_only_fields = '__all__'