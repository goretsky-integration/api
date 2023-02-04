import datetime
from enum import Enum
from typing import TypeAlias
from uuid import UUID

from pydantic import BaseModel, conset

__all__ = ('StopSaleByIngredients', 'StopSaleBySalesChannels', 'UnitUUIDs')

UnitUUIDs: TypeAlias = conset(min_items=1, max_items=30)


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
