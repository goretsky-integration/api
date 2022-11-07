import uuid

from pydantic import BaseModel, Field, NonNegativeInt, NonNegativeFloat

__all__ = (
    'UnitProductivityBalanceStatistics',
    'UnitRestaurantCookingTimeStatistics',
    'UnitDeliverySpeedStatistics',
)


class UnitProductivityBalanceStatistics(BaseModel):
    unit_uuid: uuid.UUID = Field(
        description='UUID пиццерии',
    )
    sales_per_labor_hour: NonNegativeInt = Field(
        description='Производительность кухни',
    )
    orders_per_labor_hour: NonNegativeFloat = Field(
        description="Производительность доставки",
    )
    stop_sale_duration_in_seconds: NonNegativeInt = Field(
        description='Продолжительность стопа продаж с типом "полная остановка" за текующие сутки',
    )


class UnitRestaurantCookingTimeStatistics(BaseModel):
    unit_uuid: uuid.UUID = Field(
        description='UUID пиццерии',
    )
    average_tracking_pending_and_cooking_time: int


class UnitDeliverySpeedStatistics(BaseModel):
    unit_uuid: uuid.UUID
    average_cooking_time: int = 0
    average_delivery_order_fulfillment_time: int = 0
    average_heated_shelf_time: int = 0
    average_order_trip_time: int = 0