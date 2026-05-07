from rest_framework import serializers

from users.enums import UserRole
from users.models import CustomUser, UserProfile
from users.serializers.user_profile import UserProfileReadSerializer

__all__ = ['GetUserPublicSerializer']


class GetUserPublicSerializer(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'gender',
            'is_active',
            'created_at',
            'user_profile',
        )
        read_only_fields = fields

    def get_user_profile(self, obj: CustomUser):
        if UserRole(obj.role) != UserRole.Client:
            return None
        try:
            profile = obj.user_profile
        except UserProfile.DoesNotExist:
            return None
        return UserProfileReadSerializer(profile, context=self.context).data
