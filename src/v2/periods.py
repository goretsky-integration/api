import datetime
from dataclasses import dataclass

__all__ = (
    'get_moscow_now',
    'Period',
    'round_to_hours',
)


def get_moscow_now() -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)


def round_to_hours(dt: datetime.datetime) -> datetime.datetime:
    hours = dt.hour
    if hours != 23:
        hours += 1
    return datetime.datetime(dt.year, dt.month, dt.day, hours)


@dataclass(frozen=True, slots=True)
class Period:
    start: datetime.datetime
    end: datetime.datetime

    @classmethod
    def today(cls) -> 'Period':
        now = get_moscow_now()
        start = datetime.datetime(now.year, now.month, now.day)
        return cls(start=start, end=now)

    @classmethod
    def week_before_to_this_time(cls) -> 'Period':
        week_before = get_moscow_now() - datetime.timedelta(days=7)
        start = datetime.datetime(week_before.year, week_before.month, week_before.day)
        return cls(start=start, end=week_before)

    @classmethod
    def week_before(cls) -> 'Period':
        week_before = get_moscow_now() - datetime.timedelta(days=7)
        start = datetime.datetime(week_before.year, week_before.month, week_before.day)
        end = datetime.datetime(week_before.year, week_before.month, week_before.day, 23, 59, 59)
        return cls(start, end)
