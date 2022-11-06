import datetime
from typing import TypeVar

from pydantic import validator, BaseModel

__all__ = (
    'StopSale',
    'StopSaleByStreet',
    'StopSaleBySector',
)

T = TypeVar('T')


def get_or_none(value: T) -> T | None:
    return value or None


class StopSale(BaseModel):
    unit_name: str
    started_at: datetime.datetime
    ended_at: datetime.datetime | None
    staff_name_who_stopped: str
    staff_name_who_resumed: str | None

    _get_or_none = validator('staff_name_who_resumed', 'ended_at', allow_reuse=True)(get_or_none)


class StopSaleByStreet(StopSale):
    sector: str
    street: str

    @validator('started_at', 'ended_at', pre=True)
    def str_to_dt(cls, value: str | None) -> datetime.datetime | None:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        return value


class StopSaleBySector(StopSale):
    sector: str

    @validator('started_at', 'ended_at', pre=True)
    def str_to_dt(cls, value: str | None) -> datetime.datetime | None:
        if isinstance(value, str):
            return datetime.datetime.strptime(value, '%d.%m.%Y %H:%M')
        return value
