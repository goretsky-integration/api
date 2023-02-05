import datetime
from dataclasses import dataclass

from pydantic import BaseModel, validator

__all__ = (
    'UnitsRevenueStatistics',
    'UnitRevenue',
    'TotalRevenue',
    'RevenueStatisticsReport',
    'UnitBonusSystemStatistics',
    'CheatedOrder',
    'CheatedOrders',
)


@dataclass(frozen=True, slots=True)
class UnitRevenue:
    unit_id: int
    today: int
    from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class TotalRevenue:
    today: int
    from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class UnitsRevenueStatistics:
    units: list[UnitRevenue]
    total: TotalRevenue


@dataclass(frozen=True, slots=True)
class RevenueStatisticsReport:
    results: UnitsRevenueStatistics
    errors: list[int]


@dataclass(frozen=True, slots=True)
class UnitBonusSystemStatistics:
    unit_id: int
    orders_with_phone_numbers_count: int = 0
    orders_with_phone_numbers_percent: int = 0
    total_orders_count: int = 0


class CheatedOrder(BaseModel):
    number: str
    created_at: datetime.datetime

    @validator('created_at', pre=True)
    def str_date_to_datetime(cls, value: str | datetime.datetime) -> datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%d.%m.%Y %H:%M')


@dataclass(frozen=True, slots=True)
class CheatedOrders:
    unit_name: str
    orders: list[CheatedOrder]
    phone_number: str
