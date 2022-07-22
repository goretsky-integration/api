import uuid

from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt

from models import UnitOperationalStatisticsForTodayAndWeekBefore
from models.private_dodo_api import UnitDeliveryStatistics, SalesChannel

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
    'RestaurantOrdersStatistics',
    'UnitDeliveryStatisticsExtended',
    'RevenueStatistics',
    'UnitsRevenueMetadata',
    'UnitBeingLateCertificates',
    'UnitBeingLateCertificatesTodayAndWeekBefore',
    'UnitDeliverySpeed',
    'UnitKitchenPerformance',
    'OperationalStatisticsBatch',
    'KitchenPerformanceStatistics',
    'UnitDeliveryPerformance',
    'DeliveryPerformanceStatistics',
    'HeatedShelfStatistics',
    'UnitHeatedShelf',
    'UnitCouriers',
    'CouriersStatistics',
    'KitchenProductionStatistics',
    'UnitKitchenProduction',
    'UnitOrdersHandoverTime',
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


class RevenueStatistics(BaseModel):
    units: list[RevenueForTodayAndWeekBeforeStatistics]
    metadata: UnitsRevenueMetadata
    error_unit_ids: list[int]


class RestaurantOrdersStatistics(BaseModel):
    department: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percentage: int
    total_orders_count: int


class UnitDeliveryStatisticsExtended(UnitDeliveryStatistics):
    orders_for_courier_count_per_hour: NonNegativeFloat
    delivery_with_courier_app_percent: NonNegativeFloat
    couriers_workload: NonNegativeFloat


class UnitBeingLateCertificates(BaseModel):
    unit_id: int
    unit_name: str
    being_late_certificates_count: int


class UnitBeingLateCertificatesTodayAndWeekBefore(BaseModel):
    unit_id: int
    unit_name: str
    certificates_today_count: int
    certificates_week_before_count: int


class UnitDeliverySpeed(BaseModel):
    unit_uuid: uuid.UUID
    unit_name: str
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int


class UnitKitchenPerformance(BaseModel):
    unit_id: int
    revenue_per_hour: int
    revenue_delta_from_week_before: int


class KitchenPerformanceStatistics(BaseModel):
    units: list[UnitKitchenPerformance]
    error_unit_ids: list[int]


class OperationalStatisticsBatch(BaseModel):
    units: list[UnitOperationalStatisticsForTodayAndWeekBefore]
    error_unit_ids: list[int]


class UnitDeliveryPerformance(BaseModel):
    unit_id: int
    orders_for_courier_count_per_hour_today: float
    orders_for_courier_count_per_hour_week_before: float
    delta_from_week_before: int


class DeliveryPerformanceStatistics(BaseModel):
    units: list[UnitDeliveryPerformance]
    error_unit_ids: list[int]


class UnitHeatedShelf(BaseModel):
    unit_id: int
    average_awaiting_time: int
    awaiting_orders_count: int


class HeatedShelfStatistics(BaseModel):
    units: list[UnitHeatedShelf]
    error_unit_ids: list[int]


class UnitCouriers(BaseModel):
    unit_id: int
    in_queue_count: int
    total_count: int


class CouriersStatistics(BaseModel):
    units: list[UnitCouriers]
    error_unit_ids: list[int]


class UnitKitchenProduction(BaseModel):
    unit_id: int
    average_cooking_time: int


class KitchenProductionStatistics(BaseModel):
    units: list[UnitKitchenProduction]
    error_unit_ids: list[int]


class UnitOrdersHandoverTime(BaseModel):
    unit_uuid: uuid.UUID
    unit_name: str
    average_tracking_pending_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    sales_channels: list[SalesChannel]
