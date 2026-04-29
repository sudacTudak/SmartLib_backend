from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from work_loan.models import WorkLoan
from works.models import WorkItem
from library.models import LibraryBranch
from users.models import CustomUser


class WorkLoanWriteSerializer(serializers.ModelSerializer):
    work_item_id = serializers.PrimaryKeyRelatedField(queryset=WorkItem.objects.all(), source='work_item')
    library_branch_id = serializers.PrimaryKeyRelatedField(queryset=LibraryBranch.objects.all(), source='library_branch')
    client_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.get_clients(), source='client')
    created_by_id = serializers.PrimaryKeyRelatedField(read_only=True, source='created_by')

    class Meta:
        model = WorkLoan
        fields = (
            'work_item_id',
            'library_branch_id',
            'client_id',
            'client_phone',
            'client_email',
            'client_fullname',
            'loaned_till',
            'created_by_id',
        )

    def update(self):
        raise ValueError('Для данной модели не предусмотрен полный update')

    def create(self, validated_data):
        request = self.context.get('request')
        user = None if request is None else getattr(request, 'user', None)

        if user is None or not getattr(user, 'is_authenticated', False):
            raise NotAuthenticated('Только авторизованный сотрудник может создать WorkLoan.')

        if not user.is_staff_user:
            raise PermissionDenied('Только сотрудник может создать WorkLoan.')

        validated_data['created_by'] = user
        return WorkLoan.objects.create_work_loan(validated_data)


class WorkLoanReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkLoan
        fields = (
            'id',
            'work_item_id',
            'library_branch_id',
            'client_id',
            'client_phone',
            'client_email',
            'client_fullname',
            'loaned_till',
            'status',
            'closed_at',
            'created_at',
            'updated_at',
            'created_by_id',
        )
        read_only_fields = fields


class WorkLoanProlongSerializer(serializers.Serializer):
    prolong_time = serializers.IntegerField(min_value=86_400_000)

