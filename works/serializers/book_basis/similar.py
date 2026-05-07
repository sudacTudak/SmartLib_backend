from rest_framework import serializers

from works.serializers.book_basis.serializer import WorkSerializer

__all__ = ['WorkSimilarSerializer']


class WorkSimilarSerializer(WorkSerializer):
    similarity_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = WorkSerializer.Meta.model
        fields = (*WorkSerializer.Meta.fields, 'similarity_score')
        read_only_fields = (*WorkSerializer.Meta.read_only_fields, 'similarity_score')

