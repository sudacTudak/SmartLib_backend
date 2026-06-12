from common_core.enums import AppIntEnum

__all__ = ['WorkReservationStatus']


class WorkReservationStatus(AppIntEnum):
    Open = 0
    Closed = 1
    ClientDeclined = 2
    StaffDeclined = 3

    def is_open(self):
        return self == self.Open

    def is_closed(self):
        return self == self.Closed

    def is_terminal(self):
        return self in (self.Closed, self.ClientDeclined, self.StaffDeclined)
