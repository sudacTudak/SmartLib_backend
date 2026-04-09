import datetime
from typing import TypeVar, cast

from django.core.exceptions import BadRequest
from django.db.models.manager import Manager
from django.db import transaction

from .queryset import BookLoanQuerySet
from typing import TYPE_CHECKING

from ...enums import BookLoanStatus

__all__ = ['BookLoanManager', 'BookLoanManagerType']


class BookLoanManager(Manager.from_queryset(BookLoanQuerySet)):
    def create_book_loan(self, created_data: dict):
        from .models import BookLoan
        from books_model.models import Book

        try:
            with transaction.atomic():
                book = cast(Book, created_data.get('book'))

                if book.available_count == 0:
                    raise BadRequest(f'Книги {Book} нет в наличии')

                loan = cast(BookLoan, self.model(**created_data))
                loan.save()

                book.available_count -= 1
                book.save()

                return loan
        except (BadRequest,) as e:
            print(f'{e!r}')
            raise e from e

    if TYPE_CHECKING:
        from .models import BookLoan
        async def close_book_loan(self, loan: BookLoan):
            ...

        async def prolong_book_loan(self, book_loan: BookLoan, *, prolong_for_ms: int):
            ...
    else:
        def close_book_loan(self, loan):
            from .models import BookLoan
            from books_model.models import Book

            try:
                with transaction.atomic():
                    book_loan = cast(BookLoan, loan)
                    book = book_loan.book

                    if book.available_count >= book.total_count:
                        raise ValueError(f'f{book} total_count превышает available_count')

                    book_loan.status = BookLoanStatus.Closed
                    book_loan.closed_at = datetime.time()
                    book_loan.asave()

                    book.available_count += 1
                    book.asave()

                    return book_loan
            except (ValueError,) as e:
                print(f'{e!r}')
                raise e from e

        def prolong_book_loan(self, book_loan, *, prolong_for_ms: int):
            from .models import BookLoan

            loan = cast(BookLoan, book_loan)
            loan.loaned_till = loan.loaned_till + datetime.timedelta(milliseconds=prolong_for_ms)
            loan.save()
            return loan


class _BookLoanManager(BookLoanManager, BookLoanQuerySet):
    pass


BookLoanManagerType = TypeVar('BookLoanManagerType', bound=_BookLoanManager)
