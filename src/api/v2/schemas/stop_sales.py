import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

__all__ = ('StopSaleByIngredients', 'StopSaleBySalesChannels')


class StopSale(BaseModel):
    id: UUID
    unit_uuid: UUID
    unit_name: str
    reason: str
    started_at: datetime.datetime
    ended_at: datetime.datetime | None
    stopped_by_user_id: UUID
    resumed_by_user_id: UUID | None

    class Meta:
        use_enum_values = True


class StopSaleByIngredients(StopSale):
    ingredient_name: str


class SalesChannel(Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class ChannelStopType(Enum):
    COMPLETE = 'Complete'
    REDIRECTION = 'Redirection'


class StopSaleBySalesChannels(StopSale):
    sales_channel_name: SalesChannel
    channel_stop_type: ChannelStopType
