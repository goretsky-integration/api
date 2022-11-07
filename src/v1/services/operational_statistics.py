from typing import Iterable

from v1 import models

__all__ = (
    'calculate_total_revenue',
    'calculate_units_revenue',
    'calculate_percent_from_week_before',
)


def calculate_percent_from_week_before(now: int, week_before: int) -> int:
    if week_before == 0:
        return 0
    return round(now / week_before * 100) - 100


def calculate_units_revenue(
        units: Iterable[models.UnitOperationalStatisticsForTodayAndWeekBefore],
) -> list[models.UnitRevenue]:
    return [
        models.UnitRevenue(
            today=unit.today.revenue,
            from_week_before_in_percents=calculate_percent_from_week_before(
                now=unit.today.revenue,
                week_before=unit.week_before_to_this_time.revenue,
            )
        ) for unit in units
    ]


def calculate_total_revenue(
        units: Iterable[models.UnitOperationalStatisticsForTodayAndWeekBefore],
) -> models.TotalRevenue:
    total_revenue_today = sum(unit.today.revenue for unit in units)
    total_revenue_week_before = sum(unit.week_before_to_this_time.revenue for unit in units)
    from_week_before_in_percents = calculate_percent_from_week_before(total_revenue_today, total_revenue_week_before)
    return models.TotalRevenue(
        today=total_revenue_today,
        from_week_before_in_percents=from_week_before_in_percents,
    )