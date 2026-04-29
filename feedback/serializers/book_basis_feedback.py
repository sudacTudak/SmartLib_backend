from django.shortcuts import get_object_or_404
from rest_framework import serializers

from works.models import Work
from feedback.models import WorkFeedback

__all__ = ['WorkFeedbackSerializer']


class WorkFeedbackSerializer(serializers.ModelSerializer):
    client_id = serializers.UUIDField(read_only=True)

    class Meta:
        model = WorkFeedback
        fields = ('id', 'work_id', 'client_id', 'score', 'comment', 'created_at', 'updated_at')
        read_only_fields = ('id', 'client_id', 'created_at', 'updated_at')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields['work_id'].read_only = True

    def create(self, validated_data):
        work_id = validated_data.pop('work_id')
        work = get_object_or_404(Work, pk=work_id)
        request = self.context['request']
        return WorkFeedback.objects.create(
            work=work,
            client=request.user,
            **validated_data,
        )
