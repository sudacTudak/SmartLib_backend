from rest_framework import serializers

from feedback.models import LibraryBranchFeedback

__all__ = ['LibraryBranchFeedbackSerializer']


class LibraryBranchFeedbackSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = LibraryBranchFeedback
        fields = ('id', 'library_branch_id', 'client_id', 'score', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'library_branch_id', 'client_id', 'created_at', 'updated_at')
