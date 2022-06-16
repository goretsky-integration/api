from datetime import datetime

from pydantic import BaseModel

__all__ = (
    'CheatedOrder',
    'CheatedOrders',
)


class CheatedOrder(BaseModel):
    no: str
    created_at: datetime


class CheatedOrders(BaseModel):
    department: str
    orders: list[CheatedOrder]
    phone_number: int
