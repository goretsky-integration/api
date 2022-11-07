import datetime

from pydantic import validator, BaseModel

__all__ = (
    'CheatedOrder',
    'CheatedOrders',
)


class CheatedOrder(BaseModel):
    number: str
    created_at: datetime.datetime

    @validator('created_at', pre=True)
    def str_date_to_datetime(cls, value: str | datetime.datetime) -> datetime.datetime:
        if isinstance(value, datetime.datetime):
            return value
        return datetime.datetime.strptime(value, '%d.%m.%Y %H:%M')


class CheatedOrders(BaseModel):
    unit_name: str
    orders: list[CheatedOrder]
    phone_number: str
