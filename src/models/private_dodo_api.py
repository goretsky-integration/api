import uuid

from pydantic import BaseModel, Field, NonNegativeInt

__all__ = (
    'UnitDeliveryStatistics',
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
