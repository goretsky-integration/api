from typing import TypeAlias

from pydantic import BaseModel, conset

__all__ = (
    'UnitIDs',
    'StockBalanceStatistics',
)

UnitIDs: TypeAlias = conset(int, min_items=1, max_items=30)


class IngredientStocksBalance(BaseModel):
    unit_id: int
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


class StockBalanceStatistics(BaseModel):
    units: list[IngredientStocksBalance]
    error_unit_ids: list[int]
