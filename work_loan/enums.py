from common_core.enums import AppIntEnum

__all__ = ['WorkLoanStatus', 'BookLoanStatus']


class WorkLoanStatus(AppIntEnum):
    Open = 0,
    Closed = 1,

    def is_closed(self):
        return self == self.Closed

    def is_open(self):
        return self == self.Open


# Backward-compatible alias for historical migrations that import `BookLoanStatus`.
BookLoanStatus = WorkLoanStatus

