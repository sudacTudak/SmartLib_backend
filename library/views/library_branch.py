from django.db.models import Avg, Count, QuerySet
from rest_framework.permissions import SAFE_METHODS, IsAdminUser

from common_core.classes import ViewSetBase
from library.models import LibraryBranch
from library.serializers import LibraryBranchSerializer
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, UpdateModelMixin
from typing import cast
from django.db import transaction
from works.models import WorkItem, Work


class LibraryBranchViewSet(ViewSetBase[QuerySet[LibraryBranch]], RetrieveModelMixin, ListModelMixin, CreateModelMixin,
                           UpdateModelMixin):
    serializer_class = LibraryBranchSerializer
    queryset = LibraryBranch.objects.all()

    def get_queryset(self) -> QuerySet[LibraryBranch]:
        qs = super().get_queryset()
        if self.request.method in SAFE_METHODS:
            qs = qs.annotate(
                rating_avg=Avg('feedbacks__score'),
                rating_count=Count('feedbacks', distinct=True),
            )
        return qs

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return []
        return [IsAdminUser()]

    def perform_create(self, serializer):
        serializer = cast(LibraryBranchSerializer, serializer)

        with transaction.atomic():
            library_branch = cast(LibraryBranch, serializer.save())
            works_qs = Work.objects.all()

            WorkItem.objects.bulk_create(
                WorkItem(library_branch=library_branch, work=work, available_count=0, total_count=0) for work in
                works_qs)
