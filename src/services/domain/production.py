import collections
import datetime
import statistics
from typing import Iterable, TypeVar, DefaultDict, Generator
from uuid import UUID

from models.domain import production as production_models
from models.external_api_responses.dodo_is_api import delivery as dodo_is_api_delivery_models
from models.external_api_responses.dodo_is_api import production as dodo_is_api_production_models

T = TypeVar('T')
SSv2 = TypeVar('SSv2', bound=dodo_is_api_production_models.StopSale)


def group_by_unit_uuids(items: Iterable[T]) -> DefaultDict[UUID, list[T]]:
    uuid_to_items = collections.defaultdict(list)
    for item in items:
        uuid_to_items[item.unit_uuid].append(item)
    return uuid_to_items


def filter_dine_in_sales_channel_orders(orders: Iterable[dodo_is_api_production_models.OrdersHandoverTime]):
    return [order for order in orders
            if order.sales_channel.name == dodo_is_api_production_models.SalesChannel.DINE_IN.name]


def calculate_average_tracking_pending_and_cooking_time(
        orders: Iterable[dodo_is_api_production_models.OrdersHandoverTime],
) -> int:
    average_tracking_pending_and_cooking_time = 0
    orders = filter_dine_in_sales_channel_orders(orders)
    if orders:
        average_cooking_time = statistics.mean([order.cooking_time for order in orders])
        average_tracking_pending_time = statistics.mean([order.tracking_pending_time for order in orders])
        average_tracking_pending_and_cooking_time = average_cooking_time + average_tracking_pending_time
    return average_tracking_pending_and_cooking_time


def calculate_unit_total_stop_duration(
        stop_sales: Iterable[SSv2],
        now: datetime.datetime
) -> int | float:
    stop_duration = 0
    for stop_sale in stop_sales:
        ended_at = stop_sale.ended_at if stop_sale.is_resumed else now
        stop_duration += (ended_at - stop_sale.started_at).total_seconds()
    return stop_duration


def calculate_unit_productivity_balance(
        *,
        unit_uuid: UUID,
        unit_uuid_to_productivity_statistics: dict[UUID, dodo_is_api_production_models.UnitProductivityStatistics],
        unit_uuid_to_delivery_statistics: dict[UUID, dodo_is_api_delivery_models.UnitDeliveryStatistics],
        stop_sales_grouped_by_unit_uuid: dict[UUID, Iterable[dodo_is_api_production_models.StopSaleBySalesChannels]],
        now: datetime.datetime,
) -> production_models.UnitProductivityBalanceStatistics:
    sales_per_labor_hour = (unit_uuid_to_productivity_statistics[unit_uuid].sales_per_labor_hour
                            if unit_uuid in unit_uuid_to_productivity_statistics else 0)

    orders_per_labor_hour = (unit_uuid_to_delivery_statistics[unit_uuid].orders_per_labor_hour
                             if unit_uuid in unit_uuid_to_delivery_statistics else 0)

    stop_sales = stop_sales_grouped_by_unit_uuid.get(unit_uuid, [])
    stop_sale_duration_in_seconds = calculate_unit_total_stop_duration(stop_sales, now)

    return production_models.UnitProductivityBalanceStatistics(
        unit_uuid=unit_uuid,
        sales_per_labor_hour=sales_per_labor_hour,
        orders_per_labor_hour=orders_per_labor_hour,
        stop_sale_duration_in_seconds=stop_sale_duration_in_seconds,
    )


def filter_complete_delivery_stop_sales(
        stop_sales: Iterable[dodo_is_api_production_models.StopSaleBySalesChannels],
) -> Generator[dodo_is_api_production_models.StopSaleBySalesChannels, None, None]:
    return (
        stop_sale for stop_sale in stop_sales
        if stop_sale.channel_stop_type.name == dodo_is_api_production_models.ChannelStopType.COMPLETE.name
           and stop_sale.sales_channel_name.name == dodo_is_api_production_models.SalesChannel.DELIVERY.name
    )


def calculate_productivity_balance(
        *,
        unit_uuids,
        productivity_statistics,
        delivery_statistics,
        stop_sales: Iterable[dodo_is_api_production_models.StopSaleBySalesChannels],
        now: datetime.datetime,
) -> list[production_models.UnitProductivityBalanceStatistics]:
    complete_delivery_stop_sales = filter_complete_delivery_stop_sales(stop_sales)
    stop_sales_grouped_by_unit_uuid = group_by_unit_uuids(complete_delivery_stop_sales)
    unit_uuid_to_productivity_statistics = {unit.unit_uuid: unit for unit in productivity_statistics}
    unit_uuid_to_delivery_statistics = {unit.unit_uuid: unit for unit in delivery_statistics}
    return [
        calculate_unit_productivity_balance(
            unit_uuid=unit_uuid,
            stop_sales_grouped_by_unit_uuid=stop_sales_grouped_by_unit_uuid,
            unit_uuid_to_productivity_statistics=unit_uuid_to_productivity_statistics,
            unit_uuid_to_delivery_statistics=unit_uuid_to_delivery_statistics,
            now=now
        ) for unit_uuid in unit_uuids
    ]


def calculate_restaurant_cooking_time(
        unit_uuids: Iterable[UUID],
        orders: Iterable[dodo_is_api_production_models.OrdersHandoverTime]
) -> list[production_models.UnitRestaurantCookingTimeStatistics]:
    orders_grouped_by_unit_uuid = group_by_unit_uuids(orders)
    return [
        production_models.UnitRestaurantCookingTimeStatistics(
            unit_uuid=unit_uuid,
            average_tracking_pending_and_cooking_time=calculate_average_tracking_pending_and_cooking_time(
                orders=orders_grouped_by_unit_uuid[unit_uuid]
            )
        ) for unit_uuid in unit_uuids
    ]


def unit_heated_shelf_time_statistics_factory(
        *,
        unit_uuid: UUID,
        average_heated_shelf_time: int,
) -> production_models.UnitHeatedShelfTimeStatistics:
    return production_models.UnitHeatedShelfTimeStatistics(
        unit_uuid=unit_uuid,
        average_heated_shelf_time=average_heated_shelf_time,
    )


def calculate_units_heated_shelf_time_statistics(
        production_productivity_statistics: Iterable[dodo_is_api_production_models.UnitProductivityStatistics],
) -> list[production_models.UnitHeatedShelfTimeStatistics]:
    return [
        unit_heated_shelf_time_statistics_factory(
            unit_uuid=unit.unit_uuid,
            average_heated_shelf_time=unit.avg_heated_shelf_time,
        ) for unit in production_productivity_statistics
    ]
