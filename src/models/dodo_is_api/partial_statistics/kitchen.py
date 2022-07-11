from pydantic import BaseModel

__all__ = (
    'KitchenWorkPartial',
    'UnitsKitchenPartialStatistics',
)


class ProductSpending(BaseModel):
    per_hour: float
    delta_from_week_before: int


class KitchenRevenue(BaseModel):
    per_hour: int
    delta_from_week_before: int


class Tracking(BaseModel):
    postponed: int
    in_queue: int
    in_work: int


class KitchenWorkPartial(BaseModel):
    unit_id: int
    revenue: KitchenRevenue
    product_spending: ProductSpending
    average_cooking_time: int
    tracking: Tracking


class UnitsKitchenPartialStatistics(BaseModel):
    units: list[KitchenWorkPartial]
    error_unit_ids: list[int]
