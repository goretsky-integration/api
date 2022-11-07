from pydantic import BaseModel

__all__ = (
    'UnitsRevenueStatistics',
    'RevenueStatisticsReport',
    'UnitRevenue',
    'TotalRevenue',
)


class UnitRevenue(BaseModel):
    today: int
    from_week_before_in_percents: int


class TotalRevenue(BaseModel):
    today: int
    from_week_before_in_percents: int


class UnitsRevenueStatistics(BaseModel):
    units: list[UnitRevenue]
    total: TotalRevenue


class RevenueStatisticsReport(BaseModel):
    results: UnitsRevenueStatistics
    errors: list[int]