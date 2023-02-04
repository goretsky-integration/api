from pydantic import BaseModel, NonNegativeInt, PositiveInt, NonNegativeFloat

__all__ = (
    'UnitRevenue',
    'TotalRevenue',
    'RevenueStatisticsReport',
    'UnitsRevenueStatistics',
    'UnitDeliveryPartialStatistics',
    'DeliveryPartialStatisticsReport',
    'UnitKitchenPartialStatistics',
    'KitchenPartialStatisticsReport',
    'UnitBonusSystemStatistics',
    'TripsWithOneOrder',
)


class UnitRevenue(BaseModel):
    unit_id: PositiveInt
    today: NonNegativeInt
    from_week_before_in_percents: int


class TotalRevenue(BaseModel):
    today: NonNegativeInt
    from_week_before_in_percents: int


class UnitsRevenueStatistics(BaseModel):
    units: list[UnitRevenue]
    total: TotalRevenue


class RevenueStatisticsReport(BaseModel):
    results: UnitsRevenueStatistics
    errors: list[PositiveInt]


class UnitDeliveryPartialStatistics(BaseModel):
    unit_id: PositiveInt
    heated_shelf_orders_count: NonNegativeInt
    couriers_in_queue_count: NonNegativeInt
    couriers_on_shift_count: NonNegativeInt


class DeliveryPartialStatisticsReport(BaseModel):
    results: list[UnitDeliveryPartialStatistics]
    errors: list[PositiveInt]


class UnitKitchenPartialStatistics(BaseModel):
    unit_id: PositiveInt
    sales_per_labor_hour_today: NonNegativeInt
    from_week_before_percent: int
    total_cooking_time: NonNegativeInt


class KitchenPartialStatisticsReport(BaseModel):
    results: list[UnitKitchenPartialStatistics]
    errors: list[PositiveInt]


class UnitBonusSystemStatistics(BaseModel):
    unit_id: PositiveInt
    orders_with_phone_numbers_count: NonNegativeInt
    orders_with_phone_numbers_percent: NonNegativeInt
    total_orders_count: NonNegativeInt


class TripsWithOneOrder(BaseModel):
    unit_name: str
    percentage: NonNegativeFloat
