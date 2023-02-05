from dataclasses import dataclass
from pydantic import BaseModel

__all__ = (
    'StockBalance',
    'StockBalanceStatistics',
)


class StockBalance(BaseModel):
    unit_id: int
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


class StockBalanceStatistics(BaseModel):
    units: list[StockBalance]
    error_unit_ids: list[int]
