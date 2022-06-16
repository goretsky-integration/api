from datetime import datetime, timedelta


def get_moscow_datetime_now() -> datetime:
    return datetime.utcnow() + timedelta(hours=3)
