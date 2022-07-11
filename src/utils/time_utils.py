from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Period:
    from_datetime: datetime | None = None
    to_datetime: datetime | None = None

    def __post_init__(self):
        if self.from_datetime is None:
            self.from_datetime = self.new_today().from_datetime
        if self.to_datetime is None:
            self.to_datetime = self.new_today().to_datetime

    @staticmethod
    def now() -> datetime:
        return datetime.utcnow() + timedelta(hours=3)

    @classmethod
    def new_today(cls) -> 'Period':
        now = cls.now()
        from_datetime = datetime(now.year, now.month, now.day)
        return cls(from_datetime=from_datetime, to_datetime=now)

    @classmethod
    def new_week_ago(cls) -> 'Period':
        now = cls.now() - timedelta(days=7)
        from_datetime = datetime(now.year, now.month, now.day)
        return cls(from_datetime=from_datetime, to_datetime=now)
