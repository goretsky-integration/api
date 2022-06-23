import models
from utils.calculations import (
    calculate_revenue_delta_in_percents,
    calculate_couriers_workload,
    calculate_delivery_with_courier_app_percent,
    calculate_orders_for_courier_count_per_hour,
)

__all__ = (
    'weekly_operational_statistics_to_revenue_statistics',
    'extend_unit_delivery_statistics',
)


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


def extend_unit_delivery_statistics(
        delivery_statistics: models.UnitDeliveryStatistics
) -> models.UnitDeliveryStatisticsExtended:
    return models.UnitDeliveryStatisticsExtended(
        **delivery_statistics.dict(by_alias=True),
        orders_for_courier_count_per_hour=calculate_orders_for_courier_count_per_hour(
            delivery_statistics.delivery_orders_count,
            delivery_statistics.couriers_shifts_duration,
        ),
        delivery_with_courier_app_percent=calculate_delivery_with_courier_app_percent(
            delivery_statistics.orders_with_courier_app_count,
            delivery_statistics.delivery_orders_count,
        ),
        couriers_workload=calculate_couriers_workload(
            delivery_statistics.trips_duration,
            delivery_statistics.couriers_shifts_duration,
        )
    )
