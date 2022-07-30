from pydantic import BaseModel

__all__ = (
    'StockBalance',
    'StockBalanceStatistics',
)


class StockBalance(BaseModel):
    unit_id: int
    ingredient_name: str
    days_left: int


class StockBalanceStatistics(BaseModel):
    units: list[StockBalance]
    error_unit_ids: list[int]
