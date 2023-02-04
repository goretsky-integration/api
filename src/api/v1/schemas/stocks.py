from pydantic import BaseModel

__all__ = (
    'StockBalanceStatistics',
)


class IngredientStocksBalance(BaseModel):
    unit_id: int
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


class StockBalanceStatistics(BaseModel):
    units: list[IngredientStocksBalance]
    error_unit_ids: list[int]
