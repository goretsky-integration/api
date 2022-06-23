from pydantic import BaseModel, validator

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
    'RestaurantOrdersStatistics',
    'KitchenRevenue',
    'KitchenStatistics',
    'Tracking',
    'ProductSpending',
)


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: int


class RestaurantOrdersStatistics(BaseModel):
    department: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percentage: int
    total_orders_count: int


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


class KitchenStatistics(BaseModel):
    unit_id: int
    revenue: KitchenRevenue
    product_spending: ProductSpending
    average_cooking_time: int
    tracking: Tracking
