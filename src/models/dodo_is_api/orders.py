from datetime import datetime

from pydantic import BaseModel, validator

__all__ = (
    'UnitBonusSystem',
    'CheatedOrder',
    'CheatedOrders',
)


class UnitBonusSystem(BaseModel):
    unit_name: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: float
    total_orders_count: int


class CheatedOrder(BaseModel):
    number: str
    created_at: datetime

    @validator('created_at', pre=True)
    def str_date_to_datetime(cls, value: str | datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        return datetime.strptime(value, '%d.%m.%Y %H:%M')


class CheatedOrders(BaseModel):
    unit_name: str
    orders: list[CheatedOrder]
    phone_number: str
