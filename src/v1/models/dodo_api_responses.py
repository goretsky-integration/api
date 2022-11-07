import datetime

from pydantic import BaseModel, Field

__all__ = (
    'OperationalStatistics',
    'UnitOperationalStatisticsForTodayAndWeekBefore',
    'UnitBeingLateCertificates',
)


class OperationalStatistics(BaseModel):
    stationary_revenue: int = Field(..., alias='stationaryRevenue')
    stationary_order_count: int = Field(..., alias='stationaryOrderCount')
    delivery_revenue: int = Field(..., alias='deliveryRevenue')
    delivery_order_count: int = Field(..., alias='deliveryOrderCount')
    revenue: int = Field(..., alias='revenue')
    order_count: int = Field(..., alias='orderCount')
    avg_check: float = Field(..., alias='avgCheck')


class UnitOperationalStatisticsForTodayAndWeekBefore(BaseModel):
    unit_id: int = Field(..., alias='unitId')
    date: datetime.datetime
    today: OperationalStatistics
    week_before: OperationalStatistics = Field(..., alias='weekBefore')
    yesterday_to_this_time: OperationalStatistics = Field(..., alias='yesterdayToThisTime')
    yesterday: OperationalStatistics = Field(..., alias='yesterday')
    week_before_to_this_time: OperationalStatistics = Field(..., alias='weekBeforeToThisTime')

    class Config:
        allow_population_by_field_name = True


class UnitBeingLateCertificates(BaseModel):
    unit_id: int
    unit_name: str
    certificates_count: int
