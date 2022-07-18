from datetime import datetime

from pydantic import BaseModel, validator

from models.validators import get_or_none

__all__ = (
    'StopSalesByStreet',
    'StopSalesBySector',
)


class StopSalesByCookies(BaseModel):
    unit_name: str
    started_at: datetime
    ended_at: datetime | None
    staff_name_who_stopped: str
    staff_name_who_resumed: str | None

    _get_or_none = validator(
        'staff_name_who_resumed',
        'ended_at',
        allow_reuse=True,
    )(get_or_none)


class StopSalesByStreet(StopSalesByCookies):
    sector: str
    street: str

    @validator(
        'started_at',
        'ended_at',
        pre=True,
    )
    def str_to_dt(cls, value: str | None) -> datetime | None:
        if isinstance(value, str):
            return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        return value


class StopSalesBySector(StopSalesByCookies):
    sector: str

    @validator(
        'started_at',
        'ended_at',
        pre=True,
    )
    def str_to_dt(cls, value: str | None) -> datetime | None:
        if isinstance(value, str):
            return datetime.strptime(value, '%d.%m.%Y %H:%M')
        return value
