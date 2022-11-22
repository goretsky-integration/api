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
    stopped_by_user_id: uuid.UUID = Field(alias='stoppedByUserId')
    resumed_by_user_id: uuid.UUID | None = Field(alias='resumedByUserId')

    class Meta:
        use_enum_values = True


class StopSaleByIngredients(StopSale):
    ingredient_name: str = Field(alias='ingredientName')


class StopSaleBySalesChannels(StopSale):
    sales_channel_name: SalesChannel = Field(alias='salesChannelName')
