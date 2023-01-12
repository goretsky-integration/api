import collections
import statistics
import uuid
from typing import TypeVar, Iterable, DefaultDict

from v2 import models

T = TypeVar('T')


def remove_duplicated_orders(orders: Iterable[models.OrdersHandoverTime]) -> tuple[models.OrdersHandoverTime, ...]:
    unique_orders: dict[uuid.UUID, models.OrdersHandoverTime] = {order.order_id: order for order in orders}
    return tuple(unique_orders.values())


def group_by_unit_uuids(items: Iterable[T]) -> DefaultDict[uuid.UUID, list[T]]:
    uuid_to_items = collections.defaultdict(list)
    for item in items:
        uuid_to_items[item.unit_uuid].append(item)
    return uuid_to_items


def calculate_average_tracking_pending_and_cooking_time(
        orders: Iterable[models.OrdersHandoverTime],
) -> int:
    average_tracking_pending_and_cooking_time = 0
    # TODO pass orders only from "dine-in" sales channel
    if orders:
        average_cooking_time = statistics.mean(
            [order.cooking_time for order in orders
             if order.sales_channel.name == models.SalesChannel.DINE_IN.name])
        average_tracking_pending_time = statistics.mean(
            [order.tracking_pending_time for order in orders
             if order.sales_channel.name == models.SalesChannel.DINE_IN.name])
        average_tracking_pending_and_cooking_time = average_cooking_time + average_tracking_pending_time
    return average_tracking_pending_and_cooking_time


def orders_to_restaurant_cooking_time_dto(
        unit_uuid: uuid.UUID,
        orders: Iterable[models.OrdersHandoverTime],
) -> models.UnitRestaurantCookingTimeStatistics:
    return models.UnitRestaurantCookingTimeStatistics(
        unit_uuid=unit_uuid,
        average_tracking_pending_and_cooking_time=calculate_average_tracking_pending_and_cooking_time(orders)
    )
