import datetime
import enum
import uuid
from typing import TypeVar

from pydantic import Field, BaseModel, validator

__all__ = (
    'StopSale',
    'SalesChannel',
    'StopSaleByIngredients',
    'StopSaleBySalesChannels',
)

T = TypeVar('T')


def get_or_none(value: T) -> T | None:
    return value or None


class SalesChannel(enum.Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class StopSale(BaseModel):
    unit_uuid: uuid.UUID = Field(alias='unitId')
    unit_name: str = Field(alias='unitName')
    reason: str = Field()
    started_at: datetime.datetime = Field(alias='startedAt')
    ended_at: datetime.datetime | None = Field(alias='endedAt')
    staff_name_who_stopped: str = Field(alias='staffNameWhoStopped')
    staff_name_who_resumed: str | None = Field(alias='staffNameWhoResumed')

    class Meta:
        use_enum_values = True

    _get_or_none = validator('staff_name_who_resumed', 'ended_at', allow_reuse=True, pre=True)(get_or_none)


class StopSaleByIngredients(StopSale):
    ingredient_name: str = Field(alias='ingredientName')


class StopSaleBySalesChannels(StopSale):
    sales_channel_name: SalesChannel = Field(alias='salesChannelName')
