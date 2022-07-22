from typing import Iterable

import models


def filter_orders_handover_time_by_sales_channels(
        orders_handover_time: Iterable[models.OrdersHandoverTime],
        allowed_sales_channels: Iterable[models.private_dodo_api.SalesChannel],
) -> list[models.OrdersHandoverTime]:
    return [order_handover_time for order_handover_time in orders_handover_time
            if order_handover_time.sales_channel in allowed_sales_channels]
