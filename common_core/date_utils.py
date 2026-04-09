import datetime

__all__ = ['get_future_from_today_date']

def get_future_from_today_date(*, milliseconds: int | None, seconds: int | None, minutes: int | None, hours: int | None, days: int | None, weeks: int | None):
    return datetime.date.today() + datetime.timedelta(milliseconds=milliseconds, seconds=seconds, minutes=minutes, hours=hours, days=days, weeks=weeks)