import datetime
from enum import Enum
from uuid import UUID

from pydantic import Field, BaseModel

__all__ = (
    'UnitDeliveryStatistics',
    'LateDeliveryVoucher',
    'LateDeliveryVoucherIssuer',
)


class UnitDeliveryStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
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


class LateDeliveryVoucherIssuer(Enum):
    SYSTEM = 'System'
    CONTACT_CENTER = 'ContactCenter'


class LateDeliveryVoucher(BaseModel):
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    order_accepted_at_local: datetime.datetime = Field(alias='orderAcceptedAtLocal')
    unit_uuid: UUID = Field(alias='unitId')
    predicted_delivery_time_local: datetime.datetime = Field(alias='predictedDeliveryTimeLocal')
    order_fulfilment_flag_at_local: datetime.datetime | None = Field(alias='orderFulfilmentFlagAtLocal')
    delivery_deadline_local: datetime.datetime = Field(alias='deliveryDeadlineLocal')
    issuer_name: LateDeliveryVoucherIssuer | None = Field(alias='issuerName')
    courier_staff_id: UUID | None = Field(alias='courierStaffId')
