import uuid

from v2 import models


def calculate_percent_from_week_before(now: int | float, week_before: int | float) -> int:
    if week_before == 0:
        return 0
    return round(now / week_before * 100) - 100


def delivery_statistics_to_delivery_speed(
        unit_delivery_statistics: models.UnitDeliveryStatistics
) -> models.UnitDeliverySpeedStatistics:
    return models.UnitDeliverySpeedStatistics(
        unit_uuid=unit_delivery_statistics.unit_uuid,
        average_cooking_time=unit_delivery_statistics.average_cooking_time,
        average_delivery_order_fulfillment_time=unit_delivery_statistics.average_delivery_order_fulfillment_time,
        average_heated_shelf_time=unit_delivery_statistics.average_heated_shelf_time,
        average_order_trip_time=unit_delivery_statistics.average_order_trip_time,
    )


def to_today_and_week_before_delivery_productivity(
        unit_uuid: uuid.UUID,
        unit_today_delivery_statistics: models.UnitDeliveryStatistics,
        unit_week_delivery_statistics: models.UnitDeliveryStatistics,
) -> models.UnitDeliveryProductivityStatistics:
    from_week_before_in_percents = calculate_percent_from_week_before(
        unit_today_delivery_statistics.orders_per_labor_hour,
        unit_week_delivery_statistics.orders_per_labor_hour
    )
    return models.UnitDeliveryProductivityStatistics(
        unit_uuid=unit_uuid,
        orders_per_courier_labour_hour_today=unit_today_delivery_statistics.orders_per_labor_hour,
        orders_per_courier_labour_hour_week_before=unit_week_delivery_statistics.orders_per_labor_hour,
        from_week_before_in_percents=from_week_before_in_percents,
    )
