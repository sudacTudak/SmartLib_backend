from rest_framework import serializers

__all__ = ['TopLoanedWorksReportRowSerializer', 'BranchLoanActivityReportRowSerializer']


class TopLoanedWorksReportRowSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    work_id = serializers.UUIDField()
    work_title = serializers.CharField()
    loan_operations_count = serializers.IntegerField()


class BranchLoanActivityReportRowSerializer(serializers.Serializer):
    rank = serializers.IntegerField()
    library_branch_id = serializers.UUIDField()
    library_branch_address = serializers.CharField()
    loan_operations_count = serializers.IntegerField()
