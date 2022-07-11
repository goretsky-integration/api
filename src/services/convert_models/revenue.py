import models
from utils.calculations import calculate_revenue_delta_in_percents, calculate_revenue_metadata

__all__ = (
    'operational_statistics_to_revenue_statistics',
)


def weekly_operational_statistics_to_revenue_statistics(
        operational_statistics: models.UnitOperationalStatisticsForTodayAndWeekBefore,
) -> models.RevenueForTodayAndWeekBeforeStatistics:
    return models.RevenueForTodayAndWeekBeforeStatistics(
        unit_id=operational_statistics.unit_id,
        today=operational_statistics.today.revenue,
        week_before=operational_statistics.week_before_to_this_time.revenue,
        delta_from_week_before=calculate_revenue_delta_in_percents(
            revenue_today=operational_statistics.today.revenue,
            revenue_week_before=operational_statistics.week_before_to_this_time.revenue,
        )
    )


def operational_statistics_to_revenue_statistics(
        operational_statistics_batch: models.OperationalStatisticsBatch,
) -> models.RevenueStatistics:
    revenue_statistics = [weekly_operational_statistics_to_revenue_statistics(operational_statistics)
                          for operational_statistics in operational_statistics_batch.units]
    revenue_metadata = calculate_revenue_metadata(revenue_statistics)
    return models.RevenueStatistics(
        revenues=revenue_statistics,
        metadata=revenue_metadata,
        error_unit_ids=operational_statistics_batch.error_unit_ids,
    )
