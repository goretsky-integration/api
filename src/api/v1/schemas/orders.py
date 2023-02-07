import datetime
from uuid import UUID

from pydantic import BaseModel, NonNegativeInt

__all__ = (
    'CheatedOrder',
    'CheatedOrders',
    'OrderByUUID',
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
    receipt_printed_at: datetime.datetime | None
    number: str
    type: str
    price: NonNegativeInt
    uuid: UUID
    courier_name: str | None
