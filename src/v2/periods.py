import datetime
from dataclasses import dataclass

__all__ = (
    'get_moscow_now',
    'Period',
)


def get_moscow_now() -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(hours=3)


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
    def week_ago(cls) -> 'Period':
        week_ago = get_moscow_now() - datetime.timedelta(days=7)
        start = datetime.datetime(week_ago.year, week_ago.month, week_ago.day)
        return cls(start=start, end=week_ago)
