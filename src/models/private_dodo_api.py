import uuid
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, NonNegativeInt, validator

from models.validators import get_or_none

__all__ = (
    'UnitDeliveryStatistics',
    'StopSalesByProduct',
    'StopSalesByIngredients',
    'StopSalesBySalesChannels',
    'OrdersHandoverTime',
    'SalesChannel',
    'UnitProductivityStatistics',
)


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

    @property
    def orders_per_labor_hour(self) -> int | float:
        if self.couriers_shifts_duration == 0:
            return 0
        return round(self.delivery_orders_count / (self.couriers_shifts_duration / 3600), 1)


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


class SalesChannel(Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class OrdersHandoverTime(BaseModel):
    unit_id: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    order_id: uuid.UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    sales_channel: SalesChannel = Field(alias='salesChannel')
    orders_tracking_start_at: datetime = Field(alias='orderTrackingStartAt')
    tracking_pending_time: int = Field(alias='trackingPendingTime')
    cooking_time: int = Field(alias='cookingTime')
    heated_shelf_time: int = Field(alias='heatedShelfTime')


class UnitProductivityStatistics(BaseModel):
    unit_uuid: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    labor_hours: int = Field(alias='laborHours')
    sales: float = Field(alias='sales')
    sales_per_labor_hour: float = Field(alias='salesPerLaborHour')
    products_per_labor_hour: float = Field(alias='productsPerLaborHour')
    avg_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    orders_per_courier_labour_hour: float = Field(alias='ordersPerCourierLabourHour')
    kitchen_speed_percentage: float = Field(alias='kitchenSpeedPercentage')
