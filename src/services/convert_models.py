import models
from services.calculations import calculate_revenue_delta_in_percents


def weekly_operational_statistics_to_revenue_statistics(
        operational_statistics: models.OperationalStatisticsForTodayAndWeekBefore,
) -> models.RevenueForTodayAndWeekBeforeStatistics:
    return models.RevenueForTodayAndWeekBeforeStatistics(
        unit_id=operational_statistics.unit_id,
        today=operational_statistics.today.revenue,
        week_before=operational_statistics.week_before.revenue,
        delta_from_week_before=calculate_revenue_delta_in_percents(
            revenue_today=operational_statistics.today.revenue,
            revenue_week_before=operational_statistics.week_before.revenue,
        )
    )
