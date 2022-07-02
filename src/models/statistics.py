from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt

from models.private_dodo_api import UnitDeliveryStatistics

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
    'RestaurantOrdersStatistics',
    'KitchenRevenue',
    'KitchenStatistics',
    'Tracking',
    'ProductSpending',
    'UnitDeliveryStatisticsExtended',
    'UnitsRevenueStatistics',
    'UnitsRevenueMetadata',
    'UnitDeliveryStatistics',
    'KitchenStatisticsBatch',
    'UnitBeingLateCertificates',
    'SingleUnitBeingLateCertificates',
)


class UnitsRevenueMetadata(BaseModel):
    total_revenue_today: NonNegativeInt
    total_revenue_week_before: NonNegativeInt
    delta_from_week_before: float


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: float


class UnitsRevenueStatistics(BaseModel):
    revenues: list[RevenueForTodayAndWeekBeforeStatistics]
    metadata: UnitsRevenueMetadata
    error_unit_ids: list[int]


class RestaurantOrdersStatistics(BaseModel):
    department: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percentage: int
    total_orders_count: int


class ProductSpending(BaseModel):
    per_hour: float
    delta_from_week_before: int


class KitchenRevenue(BaseModel):
    per_hour: int
    delta_from_week_before: int


class Tracking(BaseModel):
    postponed: int
    in_queue: int
    in_work: int


class KitchenStatistics(BaseModel):
    unit_id: int
    revenue: KitchenRevenue
    product_spending: ProductSpending
    average_cooking_time: int
    tracking: Tracking


class KitchenStatisticsBatch(BaseModel):
    kitchen_statistics: list[KitchenStatistics]
    error_unit_ids: list[int]


class UnitDeliveryStatisticsExtended(UnitDeliveryStatistics):
    orders_for_courier_count_per_hour: NonNegativeFloat
    delivery_with_courier_app_percent: NonNegativeFloat
    couriers_workload: NonNegativeFloat


class UnitBeingLateCertificates(BaseModel):
    unit_name: str
    being_late_certificates_count: int


class SingleUnitBeingLateCertificates(BaseModel):
    being_late_certificates_count: int
