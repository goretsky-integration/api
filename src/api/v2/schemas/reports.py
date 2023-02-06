from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat

__all__ = (
    'UnitProductivityBalanceStatistics',
    'UnitRestaurantCookingTimeStatistics',
    'UnitHeatedShelfTimeStatistics',
    'UnitLateDeliveryVouchers',
    'UnitDeliveryProductivityStatistics',
    'UnitDeliverySpeedStatistics',
)


class UnitProductivityBalanceStatistics(BaseModel):
    unit_uuid: UUID
    sales_per_labor_hour: NonNegativeInt
    orders_per_labor_hour: NonNegativeFloat
    stop_sale_duration_in_seconds: NonNegativeInt


class UnitRestaurantCookingTimeStatistics(BaseModel):
    unit_uuid: UUID
    average_tracking_pending_and_cooking_time: NonNegativeInt


class UnitHeatedShelfTimeStatistics(BaseModel):
    unit_uuid: UUID
    average_heated_shelf_time: NonNegativeInt


class UnitLateDeliveryVouchersTodayAndWeekBefore(BaseModel):
    unit_uuid: UUID
    certificates_count_today: NonNegativeInt
    certificates_count_week_before: NonNegativeInt


class UnitDeliveryProductivityStatistics(BaseModel):
    unit_uuid: UUID
    orders_per_courier_labour_hour_today: NonNegativeFloat
    orders_per_courier_labour_hour_week_before: NonNegativeFloat
    from_week_before_in_percents: int


class UnitDeliverySpeedStatistics(BaseModel):
    unit_uuid: UUID
    average_cooking_time: NonNegativeInt
    average_delivery_order_fulfillment_time: NonNegativeInt
    average_heated_shelf_time: NonNegativeInt
    average_order_trip_time: NonNegativeInt
