from itertools import groupby
from operator import attrgetter

from django.db.models import QuerySet
from typing import TYPE_CHECKING, TypeVar

from amenity.models.amenity_vendor.model import AmenityVendor

__all__ = ['AmenityQuerySet', 'AmenityQuerySetType']
if TYPE_CHECKING:
    from .model import Amenity

    class _Base(QuerySet[Amenity]):
        pass
else:
    class _Base(QuerySet):
        pass


class AmenityQuerySet(_Base):
    def get_all_by_vendor_id(self: "AmenityQuerySetType", vendor_id: str) -> "AmenityQuerySetType":
        return self.filter(vendor_id=vendor_id)

    def get_by_library_branch_id(self, library_branch_id: str):
        return self.filter(library_branch_id=library_branch_id)

    def get_all_grouped_by_vendor_id(self, *, exclude_empty: bool | None = True) -> dict:
        """Amenity из текущего queryset, сгруппированные по vendor_id (ключ — UUID вендора).

        exclude_empty=True (и None): только вендоры, у которых в этом queryset есть хотя бы одна Amenity.
        exclude_empty=False: все вендоры из AmenityVendor; у «пустых» — список [].
        """

        ordered = list(
            self.select_related('vendor', 'library_branch').order_by('vendor_id')
        )
        key = attrgetter('vendor_id')
        nonempty = {vid: list(group) for vid, group in groupby(ordered, key=key)}

        if exclude_empty:
            return nonempty

        return {
            vendor_id: nonempty.get(vendor_id, [])
            for vendor_id in AmenityVendor.objects.order_by('id').values_list('id', flat=True)
        }

    def get_by_library_grouped_by_vendor(self, library_branch_id: str, *, exclude_empty: bool | None = True):
        return self.filter(library_branch_id=library_branch_id).get_all_grouped_by_vendor_id(
            exclude_empty=exclude_empty
        )


AmenityQuerySetType = TypeVar('AmenityQuerySetType', bound=AmenityQuerySet)
