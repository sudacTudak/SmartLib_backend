from django.shortcuts import get_object_or_404
from rest_framework import serializers

from feedback.models import LibraryBranchFeedback
from library.models import LibraryBranch

__all__ = ['LibraryBranchFeedbackSerializer']


class LibraryBranchFeedbackSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = LibraryBranchFeedback
        fields = ('id', 'library_branch_id', 'client_id', 'score', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'client_id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['library_branch_id'].read_only = True

    def create(self, validated_data):
        library_branch_id = validated_data.pop('library_branch_id')
        library_branch = get_object_or_404(LibraryBranch, pk=library_branch_id)
        request = self.context['request']
        return LibraryBranchFeedback.objects.create(
            library_branch=library_branch,
            client=request.user,
            **validated_data,
        )
