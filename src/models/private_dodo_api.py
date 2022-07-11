import uuid
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, Field, NonNegativeInt, validator

__all__ = (
    'UnitDeliveryStatistics',
    'StopSalesByProduct',
    'StopSalesByIngredients',
    'StopSalesBySalesChannels',
    'OrdersHandoverTime',
)

T = TypeVar('T')


def get_or_none(value: T) -> T | None:
    return value or None


class UnitDeliveryStatistics(BaseModel):
    unit_id: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    average_cooking_time: NonNegativeInt = Field(alias='avgCookingTime')
    average_delivery_order_fulfillment_time: NonNegativeInt = Field(alias='avgDeliveryOrderFulfillmentTime')
    average_heated_shelf_time: NonNegativeInt = Field(alias='avgHeatedShelfTime')
    average_order_trip_time: NonNegativeInt = Field(alias='avgOrderTripTime')
    couriers_shifts_duration: NonNegativeInt = Field(alias='couriersShiftsDuration')
    delivery_orders_count: NonNegativeInt = Field(alias='deliveryOrdersCount')
    delivery_sales: NonNegativeInt = Field(alias='deliverySales')
    late_orders_count: NonNegativeInt = Field(alias='lateOrdersCount')
    orders_with_courier_app_count: NonNegativeInt = Field(alias='ordersWithCourierAppCount')
    trips_count: NonNegativeInt = Field(alias='tripsCount')
    trips_duration: NonNegativeInt = Field(alias='tripsDuration')


class StopSales(BaseModel):
    unit_id: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    reason: str = Field()
    started_at: datetime = Field(alias='startedAt')
    ended_at: datetime | None = Field(alias='endedAt')
    staff_name_who_stopped: str = Field(alias='staffNameWhoStopped')
    staff_name_who_resumed: str | None = Field(alias='staffNameWhoResumed')

    _get_or_none = validator('staff_name_who_resumed', 'ended_at', allow_reuse=True, pre=True)(get_or_none)


class StopSalesByIngredients(StopSales):
    ingredient_name: str = Field(alias='ingredientName')


class StopSalesByProduct(StopSales):
    product_name: str = Field(alias='productName')


class StopSalesBySalesChannels(StopSales):
    sales_channel_name: str = Field(alias='salesChannelName')


class OrdersHandoverTime(BaseModel):
    unit_id: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    order_id: uuid.UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    sales_channel: str = Field(alias='salesChannel')
    orders_tracking_start_at: datetime = Field(alias='orderTrackingStartAt')
    tracking_pending_time: int = Field(alias='trackingPendingTime')
    cooking_time: int = Field(alias='cookingTime')
    heated_shelf_time: int = Field(alias='heatedShelfTime')
