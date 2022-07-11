from pydantic import BaseModel

__all__ = (
    'UnitBonusSystem',
)


class UnitBonusSystem(BaseModel):
    unit_name: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: float
    total_orders_count: int
