from rest_framework import serializers

from feedback.models import BookBasisFeedback

__all__ = ['BookBasisFeedbackSerializer']


class BookBasisFeedbackSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = BookBasisFeedback
        fields = ('id', 'book_basis_id', 'client_id', 'score', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'book_basis_id', 'client_id', 'created_at', 'updated_at')
