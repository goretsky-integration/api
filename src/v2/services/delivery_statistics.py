from typing import Iterable

from v2 import models


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
