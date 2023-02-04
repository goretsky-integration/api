import datetime

from pydantic import BaseModel

__all__ = (
    'StopSaleBySector',
    'StopSaleByStreet',
)


class StopSale(BaseModel):
    unit_name: str
    started_at: datetime.datetime
    ended_at: datetime.datetime | None
    staff_name_who_stopped: str
    staff_name_who_resumed: str | None


class StopSaleByStreet(StopSale):
    sector: str
    street: str


class StopSaleBySector(StopSale):
    sector: str
