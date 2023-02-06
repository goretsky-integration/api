import collections
from typing import Iterable
from uuid import UUID

from models.domain import delivery as delivery_models
from models.external_api_responses.dodo_is_api import delivery as dodo_is_api_delivery_models
from services.domain.common import find_missing_unit_uuids

__all__ = (
    'count_late_delivery_vouchers',
    'calculate_percent_from_week_before',
    'delivery_speed_statistics_factory',
    'delivery_productivity_statistics_factory',
    'calculate_units_delivery_speed_statistics',
    'calculate_delivery_productivity_statistics',
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


def delivery_speed_statistics_factory(
        unit_delivery_statistics: dodo_is_api_delivery_models.UnitDeliveryStatistics
) -> delivery_models.UnitDeliverySpeedStatistics:
    return delivery_models.UnitDeliverySpeedStatistics(
        unit_uuid=unit_delivery_statistics.unit_uuid,
        average_cooking_time=unit_delivery_statistics.average_cooking_time,
        average_delivery_order_fulfillment_time=unit_delivery_statistics.average_delivery_order_fulfillment_time,
        average_heated_shelf_time=unit_delivery_statistics.average_heated_shelf_time,
        average_order_trip_time=unit_delivery_statistics.average_order_trip_time,
    )


def delivery_productivity_statistics_factory(
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


def blank_unit_delivery_speed_statistics_factory(unit_uuid: UUID) -> delivery_models.UnitDeliverySpeedStatistics:
    return delivery_models.UnitDeliverySpeedStatistics(
        unit_uuid=unit_uuid,
        average_delivery_order_fulfillment_time=0,
        average_cooking_time=0,
        average_heated_shelf_time=0,
        average_order_trip_time=0,
    )


def blank_unit_delivery_productivity_statistics_factory(
        unit_uuid: UUID,
) -> delivery_models.UnitDeliveryProductivityStatistics:
    return delivery_models.UnitDeliveryProductivityStatistics(
        unit_uuid=unit_uuid,
        orders_per_courier_labour_hour_today=0,
        orders_per_courier_labour_hour_week_before=0,
        from_week_before_in_percents=0,
    )


def calculate_units_delivery_speed_statistics(
        all_unit_uuids: Iterable[UUID],
        delivery_statistics: Iterable[dodo_is_api_delivery_models.UnitDeliveryStatistics]
) -> list[delivery_models.UnitDeliverySpeedStatistics]:
    delivery_speed_statistics = [
        delivery_speed_statistics_factory(unit_delivery_statistics)
        for unit_delivery_statistics in delivery_statistics
    ]
    # it is required because Dodo IS API does not return statistics of all units
    missing_unit_uuids = find_missing_unit_uuids(all_unit_uuids, items_with_unit_uuid=delivery_statistics)
    blank_delivery_statistics = [
        blank_unit_delivery_speed_statistics_factory(unit_uuid)
        for unit_uuid in missing_unit_uuids
    ]
    return delivery_speed_statistics + blank_delivery_statistics


def calculate_delivery_productivity_statistics(
        unit_uuids: Iterable[UUID],
        today_delivery_statistics: Iterable[dodo_is_api_delivery_models.UnitDeliveryStatistics],
        week_before_delivery_statistics: Iterable[dodo_is_api_delivery_models.UnitDeliveryStatistics],
) -> list[delivery_models.UnitDeliveryProductivityStatistics]:
    unit_uuid_to_today_statistics = {unit.unit_uuid: unit for unit in today_delivery_statistics}
    unit_uuid_to_week_before_statistics = {unit.unit_uuid: unit for unit in week_before_delivery_statistics}
    units_delivery_productivity: list[delivery_models.UnitDeliveryProductivityStatistics] = []
    for unit_uuid in unit_uuids:
        try:
            unit_today_delivery_statistics = unit_uuid_to_today_statistics[unit_uuid]
            unit_week_delivery_statistics = unit_uuid_to_week_before_statistics[unit_uuid]
        except KeyError:
            units_delivery_productivity.append(blank_unit_delivery_productivity_statistics_factory(unit_uuid))
        else:
            units_delivery_productivity.append(delivery_productivity_statistics_factory(
                unit_uuid, unit_today_delivery_statistics, unit_week_delivery_statistics,
            ))
    return units_delivery_productivity
