from django.db.models import QuerySet
from typing import TYPE_CHECKING, TypeVar
from django.db.models import Q, F
from django.db.models.functions import TruncDate
from django.utils import timezone
import datetime

from ...enums import BookLoanStatus

__all__ = ['BookLoanQuerySet', 'TypeBookLoanQuerySet']

if TYPE_CHECKING:
    from .models import BookLoan


    class _Base(QuerySet[BookLoan]):
        pass
else:
    class _Base(QuerySet):
        pass


class BookLoanQuerySet(_Base):
    class Filters:
        open = Q(status=BookLoanStatus.Open, closed_at__isnull=True)
        closed = Q(status=BookLoanStatus.Closed, closed_at__isnull=False)
        anonymous = Q(client_id__isnull=True)

    def active_expired(self):
        return self.filter(self.Filters.open, loaned_till__lt=timezone.localdate())

    def closed_expired(self):
        return self.filter(self.Filters.closed, loaned_till__lt=TruncDate("closed_at"))

    def by_client(self, *, client_id: str | None = None, client_phone: str | None = None,
                  client_email: str | None = None):
        if client_id is not None:
            return self.filter(client_id=client_id)

        q = Q()

        if client_email is not None:
            q |= Q(client_email=client_email)

        if client_phone is not None:
            q |= Q(client_phone=client_phone)

        if not q.children:
            return self

        return self.filter(q)

    def from_to(self, *, date_from: datetime.datetime | None = None, date_to: datetime.datetime | None = None):
        q = Q()

        if date_from is not None:
            q &= Q(created_at__gte=date_from)

        if date_to is not None:
            q &= Q(created_at__lte=date_to)

        if not q.children:
            return self

        return self.filter(q)

    def anonymous(self):
        return self.filter(self.Filters.anonymous)

    def active_by_registered_client(self, *, client_id: str):
        return self.by_client(client_id=client_id).filter(self.Filters.open)


TypeBookLoanQuerySet = TypeVar('TypeBookLoanQuerySet', bound=BookLoanQuerySet)
