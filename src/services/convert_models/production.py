import collections
import statistics
from typing import Iterable, TypeVar
from uuid import UUID

import models

T = TypeVar('T')


def group_by_unit_id_and_name(models_to_group: Iterable[T]) -> dict[tuple[UUID, str], list[T]]:
    unit_uuid_and_name_to_grouped_models = collections.defaultdict(list)
    for model_to_group in models_to_group:
        model_group_and_uuid = (model_to_group.unit_id, model_to_group.unit_name)
        grouped_models = unit_uuid_and_name_to_grouped_models[model_group_and_uuid]
        grouped_models.append(model_to_group)
    return unit_uuid_and_name_to_grouped_models


def filter_orders_handover_time_by_sales_channels(
        orders_handover_time: Iterable[models.OrdersHandoverTime],
        allowed_sales_channels: Iterable[models.private_dodo_api.SalesChannel],
) -> list[models.OrdersHandoverTime]:
    return [order_handover_time for order_handover_time in orders_handover_time
            if order_handover_time.sales_channel in allowed_sales_channels]


def calculate_units_average_orders_handover_time(
        orders_handover_time: Iterable[models.OrdersHandoverTime],
        sales_channels: Iterable[models.SalesChannel],
) -> list[models.UnitOrdersHandoverTime]:
    units_orders_handover_time: list[models.UnitOrdersHandoverTime] = []
    unit_uuid_and_name_to_orders_handover_time = group_by_unit_id_and_name(orders_handover_time)

    for (unit_uuid, unit_name), orders_handover_time in unit_uuid_and_name_to_orders_handover_time.items():
        average_tracking_pending_time = 0
        average_cooking_time = 0
        average_heated_shelf_time = 0

        if len(orders_handover_time):
            average_tracking_pending_time = statistics.mean(
                [order.tracking_pending_time for order in orders_handover_time])
            average_cooking_time = statistics.mean([order.cooking_time for order in orders_handover_time])
            average_heated_shelf_time = statistics.mean([order.heated_shelf_time for order in orders_handover_time])

        units_orders_handover_time.append(models.UnitOrdersHandoverTime(
            unit_uuid=unit_uuid,
            unit_name=unit_name,
            average_tracking_pending_time=average_tracking_pending_time,
            average_cooking_time=average_cooking_time,
            average_heated_shelf_time=average_heated_shelf_time,
            sales_channels=sales_channels,
        ))
    return units_orders_handover_time
