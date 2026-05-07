from rest_framework import serializers

from works.models import WorkItem

__all__ = ['HoldingsInBranchesReportSerializer']


class HoldingsInBranchesReportSerializer(serializers.ModelSerializer):
    library_branch_address = serializers.CharField(source='library_branch.address', read_only=True)
    work_title = serializers.CharField(source='work.title', read_only=True)
    last_supply_at = serializers.DateTimeField(read_only=True, allow_null=True)

    class Meta:
        model = WorkItem
        fields = (
            'id',
            'library_branch_address',
            'work_title',
            'available_count',
            'last_supply_at',
        )
        read_only_fields = fields
