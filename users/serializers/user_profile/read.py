from rest_framework import serializers

from users.models import UserProfile

__all__ = ['UserProfileReadSerializer']


class UserProfileReadSerializer(serializers.ModelSerializer):
    favorite_work_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='favorite_works_ordered_recent_first',
    )

    class Meta:
        model = UserProfile
        fields = ('id', 'favorite_work_ids', 'created_at', 'updated_at')
        read_only_fields = fields
