import collections
from typing import Iterable
from uuid import UUID

from models.domain import delivery as delivery_models
from models.external_api_responses.dodo_is_api import delivery as dodo_is_api_delivery_models

__all__ = (
    'count_late_delivery_vouchers',
    'calculate_percent_from_week_before',
    'delivery_statistics_to_delivery_speed',
    'to_today_and_week_before_delivery_productivity',
)


def count_late_delivery_vouchers(
        vouchers: Iterable[dodo_is_api_delivery_models.LateDeliveryVoucher],
) -> dict[UUID, int]:
    unit_uuid_to_vouchers_count = collections.defaultdict(int)
    for voucher in vouchers:
        unit_uuid_to_vouchers_count[voucher.unit_uuid] += 1
    return unit_uuid_to_vouchers_count


def calculate_percent_from_week_before(now: int | float, week_before: int | float) -> int:
    if week_before == 0:
        return 0
    return round(now / week_before * 100) - 100


def delivery_statistics_to_delivery_speed(
        unit_delivery_statistics: dodo_is_api_delivery_models.UnitDeliveryStatistics
) -> delivery_models.UnitDeliverySpeedStatistics:
    return delivery_models.UnitDeliverySpeedStatistics(
        unit_uuid=unit_delivery_statistics.unit_uuid,
        average_cooking_time=unit_delivery_statistics.average_cooking_time,
        average_delivery_order_fulfillment_time=unit_delivery_statistics.average_delivery_order_fulfillment_time,
        average_heated_shelf_time=unit_delivery_statistics.average_heated_shelf_time,
        average_order_trip_time=unit_delivery_statistics.average_order_trip_time,
    )


def to_today_and_week_before_delivery_productivity(
        unit_uuid: UUID,
        unit_today_delivery_statistics: dodo_is_api_delivery_models.UnitDeliveryStatistics,
        unit_week_delivery_statistics: dodo_is_api_delivery_models.UnitDeliveryStatistics,
) -> delivery_models.UnitDeliveryProductivityStatistics:
    from_week_before_in_percents = calculate_percent_from_week_before(
        unit_today_delivery_statistics.orders_per_labor_hour,
        unit_week_delivery_statistics.orders_per_labor_hour
    )
    return delivery_models.UnitDeliveryProductivityStatistics(
        unit_uuid=unit_uuid,
        orders_per_courier_labour_hour_today=unit_today_delivery_statistics.orders_per_labor_hour,
        orders_per_courier_labour_hour_week_before=unit_week_delivery_statistics.orders_per_labor_hour,
        from_week_before_in_percents=from_week_before_in_percents,
    )
