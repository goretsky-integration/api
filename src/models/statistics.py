from pydantic import BaseModel

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
)


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: int
