from rest_framework import serializers
from users.models import StaffProfile

__all__ = ['CreateStaffProfileSerializer']

class CreateStaffProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StaffProfile
        fields = ['library_branch', 'position']