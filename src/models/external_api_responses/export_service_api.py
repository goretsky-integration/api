import datetime
from decimal import Decimal

from pydantic import BaseModel, validator

__all__ = ('UsedPromoCode',)


class UsedPromoCode(BaseModel):
    unit_id: int
    promo_code: str
    event: str
    typical_description: str
    order_type: str
    order_status: str
    order_no: str
    ordered_at: datetime.datetime
    order_price: Decimal

    @validator('ordered_at', pre=True)
    def _parse_datetime(cls, value: str):
        return datetime.datetime.strptime(value, '%d.%m.%Y %H:%M:%S')

    @validator('order_price', pre=True)
    def _parse_price(cls, value: str) -> Decimal:
        return Decimal(value.replace(',', '.'))
