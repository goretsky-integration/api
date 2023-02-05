import collections
import statistics
from typing import Iterable, TypeVar, DefaultDict
from uuid import UUID

from models.external_api_responses.dodo_is_api import production as dodo_is_api_production_models
from models.domain import production as production_models

T = TypeVar('T')


def remove_duplicated_orders(
        orders: Iterable[dodo_is_api_production_models.OrdersHandoverTime]
) -> tuple[dodo_is_api_production_models.OrdersHandoverTime, ...]:
    unique_orders: dict[UUID, dodo_is_api_production_models.OrdersHandoverTime] = {order.order_id: order for order in
                                                                                   orders}
    return tuple(unique_orders.values())


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


def orders_to_restaurant_cooking_time_dto(
        unit_uuid: UUID,
        orders: Iterable[dodo_is_api_production_models.OrdersHandoverTime],
) -> production_models.UnitRestaurantCookingTimeStatistics:
    return production_models.UnitRestaurantCookingTimeStatistics(
        unit_uuid=unit_uuid,
        average_tracking_pending_and_cooking_time=calculate_average_tracking_pending_and_cooking_time(orders)
    )
