import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt, PositiveInt

__all__ = (
    'CheatedOrder',
    'CheatedOrders',
    'OrderByUUID',
    'UsedPromoCode',
)


class CheatedOrder(BaseModel):
    number: str
    created_at: datetime.datetime


class CheatedOrders(BaseModel):
    unit_name: str
    orders: list[CheatedOrder]
    phone_number: str


class OrderByUUID(BaseModel):
    unit_name: str
    created_at: datetime.datetime
    canceled_at: datetime.datetime
    receipt_printed_at: datetime.datetime | None
    number: str
    type: str
    price: NonNegativeInt
    uuid: UUID
    courier_name: str | None
    rejected_by_user_name: str | None


class UsedPromoCode(BaseModel):
    unit_id: PositiveInt
    promo_code: str
    event: str
    typical_description: str
    order_type: str
    order_status: str
    order_no: str
    ordered_at: datetime.datetime
    order_price: Decimal
