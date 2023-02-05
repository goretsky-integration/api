from dataclasses import dataclass

__all__ = (
    'StockBalance',
    'StockBalanceStatistics',
)


@dataclass(frozen=True, slots=True)
class StockBalance:
    unit_id: int
    ingredient_name: str
    days_left: int
    stocks_count: float | int
    stocks_unit: str


@dataclass(frozen=True, slots=True)
class StockBalanceStatistics:
    units: list[StockBalance]
    error_unit_ids: list[int]
