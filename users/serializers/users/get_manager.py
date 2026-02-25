from rest_framework import  serializers
from rest_framework.relations import PrimaryKeyRelatedField

from users.models import CustomUser, UserPermission


class GetManagerSerializer(serializers.ModelSerializer):
    user_permission = PrimaryKeyRelatedField(many=True, queryset=UserPermission.objects.all().only('code'))

    class Meta:
        model = CustomUser
        fields = '__all__'