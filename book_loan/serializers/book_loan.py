from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from book_loan.models import BookLoan
from books_model.models import Book
from library.models import LibraryBranch
from users.models import CustomUser


class BookLoanWriteSerializer(serializers.ModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book')
    library_branch_id = serializers.PrimaryKeyRelatedField(queryset=LibraryBranch.objects.all(),
                                                           source='library_branch')
    client_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.get_clients(), source='client')
    created_by_id = serializers.PrimaryKeyRelatedField(read_only=True, source='created_by')

    class Meta:
        model = BookLoan
        fields = ('book_id', 'library_branch_id', 'client_id', 'client_phone', 'client_email', 'client_fullname',
                  'loaned_till', 'created_by_id')

    def update(self):
        raise ValueError('Для данной модели не предусмотрен полный update')

    def create(self, validated_data):
        request = self.context.get('request')
        user = None if request is None else getattr(request, 'user', None)

        if user is None or not getattr(user, 'is_authenticated', False):
            raise NotAuthenticated('Только авторизованный сотрудник может создать BookLoan.')

        if not user.is_staff_user:
            raise PermissionDenied('Только сотрудник может создать BookLoan.')

        validated_data['created_by'] = user
        return BookLoan.objects.create_book_loan(validated_data)


class BookLoanReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLoan
        fields = ('id', 'book_id', 'library_branch_id', 'client_id', 'client_phone', 'client_email', 'client_fullname',
                  'loaned_till', 'status', 'closed_at', 'created_at', 'updated_at', 'created_by_id')
        read_only_fields = fields

class BookLoanProlongSerializer(serializers.Serializer):
    # целое число, временной промежуток в миллисекундах
    prolong_time = serializers.IntegerField(min_value=86_400_000)