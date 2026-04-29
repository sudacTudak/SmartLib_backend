import datetime
from typing import TypeVar, cast

from django.core.exceptions import BadRequest
from django.db.models.manager import Manager
from django.db import transaction

from .queryset import WorkLoanQuerySet
from typing import TYPE_CHECKING

from ...enums import WorkLoanStatus

__all__ = ['WorkLoanManager', 'WorkLoanManagerType']


class WorkLoanManager(Manager.from_queryset(WorkLoanQuerySet)):
    def create_work_loan(self, created_data: dict):
        from .models import WorkLoan

        try:
            with transaction.atomic():
                work_item = created_data.get('work_item')
                if work_item is None:
                    raise BadRequest('work_item is required')

                if work_item.available_count == 0:
                    raise BadRequest('Экземпляра нет в наличии')

                loan = cast(WorkLoan, self.model(**created_data))
                loan.save()

                work_item.available_count -= 1
                work_item.save()

                return loan
        except (BadRequest,) as e:
            print(f'{e!r}')
            raise e from e

    if TYPE_CHECKING:
        from .models import WorkLoan
        async def close_work_loan(self, loan: WorkLoan):
            ...

        async def prolong_work_loan(self, work_loan: WorkLoan, *, prolong_for_ms: int):
            ...
    else:
        def close_work_loan(self, loan):
            from .models import WorkLoan

            try:
                with transaction.atomic():
                    work_loan = cast(WorkLoan, loan)
                    work_item = work_loan.work_item

                    if work_item.available_count >= work_item.total_count:
                        raise ValueError(f'f{work_item} total_count превышает available_count')

                    work_loan.status = WorkLoanStatus.Closed
                    work_loan.closed_at = datetime.time()
                    work_loan.asave()

                    work_item.available_count += 1
                    work_item.asave()

                    return work_loan
            except (ValueError,) as e:
                print(f'{e!r}')
                raise e from e

        def prolong_work_loan(self, work_loan, *, prolong_for_ms: int):
            from .models import WorkLoan

            loan = cast(WorkLoan, work_loan)
            loan.loaned_till = loan.loaned_till + datetime.timedelta(milliseconds=prolong_for_ms)
            loan.save()
            return loan


class _WorkLoanManager(WorkLoanManager, WorkLoanQuerySet):
    pass


WorkLoanManagerType = TypeVar('WorkLoanManagerType', bound=_WorkLoanManager)

