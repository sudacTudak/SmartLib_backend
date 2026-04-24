from django.shortcuts import get_object_or_404
from rest_framework import serializers

from books_model.models import BookBasis
from feedback.models import BookBasisFeedback

__all__ = ['BookBasisFeedbackSerializer']


class BookBasisFeedbackSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BookBasisFeedback
        fields = ('id', 'book_basis_id', 'client_id', 'score', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'client_id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['book_basis_id'].read_only = True

    def create(self, validated_data):
        book_basis_id = validated_data.pop('book_basis_id')
        book_basis = get_object_or_404(BookBasis, pk=book_basis_id)
        request = self.context['request']
        return BookBasisFeedback.objects.create(
            book_basis=book_basis,
            client=request.user,
            **validated_data,
        )
