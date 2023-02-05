import datetime
import enum
from typing import TypeVar
from uuid import UUID

from pydantic import Field, BaseModel

__all__ = (
    'StopSale',
    'SalesChannel',
    'StopSaleByIngredients',
    'StopSaleBySalesChannels',
    'UnitProductivityStatistics',
    'OrdersHandoverTime'
)

T = TypeVar('T')


def get_or_none(value: T) -> T | None:
    return value or None


class SalesChannel(str, enum.Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class ChannelStopType(str, enum.Enum):
    COMPLETE = 'Complete'
    REDIRECTION = 'Redirection'


class StopSale(BaseModel):
    id: UUID
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    reason: str = Field()
    started_at: datetime.datetime = Field(alias='startedAt')
    ended_at: datetime.datetime | None = Field(alias='endedAt')
    stopped_by_user_id: UUID = Field(alias='stoppedByUserId')
    resumed_by_user_id: UUID | None = Field(alias='resumedByUserId')

    class Meta:
        use_enum_values = True


class StopSaleByIngredients(StopSale):
    ingredient_name: str = Field(alias='ingredientName')


class StopSaleBySalesChannels(StopSale):
    sales_channel_name: SalesChannel = Field(alias='salesChannelName')
    channel_stop_type: ChannelStopType = Field(alias='channelStopType')


class UnitProductivityStatistics(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    labor_hours: int = Field(alias='laborHours')
    sales: float = Field(alias='sales')
    sales_per_labor_hour: float = Field(alias='salesPerLaborHour')
    products_per_labor_hour: float = Field(alias='productsPerLaborHour')
    avg_heated_shelf_time: int = Field(alias='avgHeatedShelfTime')
    orders_per_courier_labour_hour: float = Field(alias='ordersPerCourierLabourHour')
    kitchen_speed_percentage: float = Field(alias='kitchenSpeedPercentage')


class OrdersHandoverTime(BaseModel):
    unit_uuid: UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    order_id: UUID = Field(alias='orderId')
    order_number: str = Field(alias='orderNumber')
    sales_channel: SalesChannel = Field(alias='salesChannel')
    orders_tracking_start_at: datetime.datetime = Field(alias='orderTrackingStartAt')
    tracking_pending_time: int = Field(alias='trackingPendingTime')
    cooking_time: int = Field(alias='cookingTime')
    heated_shelf_time: int = Field(alias='heatedShelfTime')
