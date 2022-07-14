from dataclasses import dataclass
from datetime import datetime, timedelta, date


@dataclass
class Period:
    from_datetime: datetime | None = None
    to_datetime: datetime | None = None

    def __post_init__(self):
        if self.from_datetime is None:
            self.from_datetime = self.new_today().from_datetime
        if self.to_datetime is None:
            self.to_datetime = self.new_today().to_datetime
        if isinstance(self.from_datetime, date):
            self.from_datetime = datetime(self.from_datetime.year, self.from_datetime.month, self.from_datetime.day)
        if isinstance(self.to_datetime, date):
            self.to_datetime = datetime(self.to_datetime.year, self.to_datetime.month, self.to_datetime.day)

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
