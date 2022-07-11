from typing import Iterable

import models
from utils.calculations import calculate_orders_for_courier_count_per_hour, calculate_delivery_with_courier_app_percent, \
    calculate_couriers_workload


def delivery_statistics_to_delivery_speed(
        units_delivery_statistics: Iterable[models.UnitDeliveryStatisticsExtended],
) -> list[models.UnitDeliverySpeed]:
    return [
        models.UnitDeliverySpeed(
            unit_uuid=unit_delivery_statistics.unit_id,
            unit_name=unit_delivery_statistics.unit_name,
            average_cooking_time=unit_delivery_statistics.average_cooking_time,
            average_delivery_order_fulfillment_time=unit_delivery_statistics.average_delivery_order_fulfillment_time,
            average_heated_shelf_time=unit_delivery_statistics.average_heated_shelf_time,
            average_order_trip_time=unit_delivery_statistics.average_order_trip_time,
        ) for unit_delivery_statistics in units_delivery_statistics
    ]


def delivery_statistics_to_delivery_performance(
        units_delivery_partial_statistics: models.UnitsDeliveryPartialStatistics
) -> models.DeliveryPerformanceStatistics:
    units = [
        models.UnitDeliveryPerformance(
            unit_id=statistics.unit_id,
            orders_for_courier_count_per_hour_today=statistics.performance.orders_for_courier_count_per_hour_today,
            orders_for_courier_count_per_hour_week_before=statistics.performance.orders_for_courier_count_per_hour_week_before,
            delta_from_week_before=statistics.performance.delta_from_week_before,
        ) for statistics in units_delivery_partial_statistics.units
    ]
    return models.DeliveryPerformanceStatistics(
        units=units,
        error_unit_ids=units_delivery_partial_statistics.error_unit_ids,
    )


def delivery_statistics_to_heated_shelf_time(
        units_delivery_partial_statistics: models.UnitsDeliveryPartialStatistics
) -> models.HeatedShelfStatistics:
    units = [
        models.UnitHeatedShelf(
            unit_id=statistics.unit_id,
            average_awaiting_time=statistics.heated_shelf.orders_awaiting_time,
            awaiting_orders_count=statistics.heated_shelf.orders_count,
        ) for statistics in units_delivery_partial_statistics.units
    ]
    return models.HeatedShelfStatistics(
        units=units,
        error_unit_ids=units_delivery_partial_statistics.error_unit_ids,
    )


def delivery_statistics_to_couriers_statistics(
        units_delivery_partial_statistics: models.UnitsDeliveryPartialStatistics
) -> models.CouriersStatistics:
    units = [
        models.UnitCouriers(
            unit_id=statistics.unit_id,
            in_queue_count=statistics.couriers.in_queue_count,
            total_count=statistics.couriers.total_count,
        ) for statistics in units_delivery_partial_statistics.units
    ]
    return models.CouriersStatistics(
        units=units,
        error_unit_ids=units_delivery_partial_statistics.error_unit_ids,
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
