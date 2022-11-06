import uuid

from pydantic import BaseModel, Field

__all__ = (
    'UnitProductivityStatistics',
    'UnitDeliveryStatistics',
)


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


class UnitDeliveryStatistics(BaseModel):
    unit_uuid: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    average_cooking_time: int = Field(alias='avgCookingTime')
    average_delivery_order_fulfillment_time: int = Field(alias='avgDeliveryOrderFulfillmentTime')
    average_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    average_order_trip_time: int = Field(alias='avgOrderTripTime')
    couriers_shifts_duration: int = Field(alias='couriersShiftsDuration')
    delivery_orders_count: int = Field(alias='deliveryOrdersCount')
    delivery_sales: int = Field(alias='deliverySales')
    late_orders_count: int = Field(alias='lateOrdersCount')
    orders_with_courier_app_count: int = Field(alias='ordersWithCourierAppCount')
    trips_count: int = Field(alias='tripsCount')
    trips_duration: int = Field(alias='tripsDuration')

    @property
    def orders_per_labor_hour(self) -> int | float:
        if self.couriers_shifts_duration == 0:
            return 0
        return round(self.delivery_orders_count / (self.couriers_shifts_duration / 3600), 1)
