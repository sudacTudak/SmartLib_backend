from itertools import chain

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from users.models import CustomUser
from library.models import LibraryBranch
from works.models import Work
from work_reservations.enums import WorkReservationStatus
from .models import WorkReservation

__all__ = [
    'ClientReadWorkReservationSerializer',
    'StaffReadWorkReservationSerializer',
    'WriteWorkReservationSerializer',
    'WorkReservationStatusSerializer',
    'WorkReservationProlongSerializer',
]


class ReadWorkReservationSerializer(serializers.ModelSerializer):
    class Meta:
        ALL_FIELDS = (
            'id',
            'client_id',
            'work_id',
            'library_branch_id',
            'status',
            'created_at',
            'reserved_till',
            'closed_at',
        )

        model = WorkReservation
        fields = ALL_FIELDS
        read_only_fields = ALL_FIELDS


class ClientReadWorkReservationSerializer(ReadWorkReservationSerializer):
    class Meta(ReadWorkReservationSerializer.Meta):
        fields = chain(ReadWorkReservationSerializer.Meta.ALL_FIELDS, ('index',))
        read_only_fields = chain(ReadWorkReservationSerializer.Meta.ALL_FIELDS, ('index',))


class StaffReadWorkReservationSerializer(ReadWorkReservationSerializer):
    class Meta(ReadWorkReservationSerializer.Meta):
        fields = chain(ReadWorkReservationSerializer.Meta.ALL_FIELDS, ('responsible_staff_id',))
        read_only_fields = chain(ReadWorkReservationSerializer.Meta.ALL_FIELDS, ('responsible_staff_id',))


class WriteWorkReservationSerializer(serializers.ModelSerializer):
    client_id = PrimaryKeyRelatedField(queryset=CustomUser.objects.get_clients(), source='client')
    work_id = PrimaryKeyRelatedField(queryset=Work.objects.all(), source='work')
    library_branch_id = PrimaryKeyRelatedField(queryset=LibraryBranch.objects.all(), source='library_branch')

    class Meta:
        model = WorkReservation
        fields = ('client_id', 'work_id', 'library_branch_id', 'reserved_till')

    def create(self, validated_data):
        return WorkReservation.objects.create_reservation(**validated_data)


class WorkReservationStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=WorkReservationStatus.as_django_model_choices())


class WorkReservationProlongSerializer(serializers.Serializer):
    prolong_time = serializers.IntegerField(min_value=86_400_000)
