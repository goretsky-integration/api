from pydantic import BaseModel

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
    'RestaurantOrdersStatistics',
)


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: int


class RestaurantOrdersStatistics(BaseModel):
    department: str
    orders_with_phone_numbers_amount: int
    orders_with_phone_numbers_percentage: int
    total_orders_amount: int
