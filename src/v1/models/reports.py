from pydantic import BaseModel

__all__ = (
    'UnitsRevenueStatistics',
    'RevenueStatisticsReport',
    'UnitRevenue',
    'TotalRevenue',
    'UnitDeliveryPartialStatistics',
    'DeliveryPartialStatisticsReport',
)


class UnitRevenue(BaseModel):
    today: int
    from_week_before_in_percents: int


class TotalRevenue(BaseModel):
    today: int
    from_week_before_in_percents: int


class UnitsRevenueStatistics(BaseModel):
    units: list[UnitRevenue]
    total: TotalRevenue


class RevenueStatisticsReport(BaseModel):
    results: UnitsRevenueStatistics
    errors: list[int]


class UnitDeliveryPartialStatistics(BaseModel):
    unit_id: int
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


class DeliveryPartialStatisticsReport(BaseModel):
    results: list[UnitDeliveryPartialStatistics]
    errors: list[int]
