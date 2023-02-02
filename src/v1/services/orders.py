from typing import Iterable, Sequence

import pandas as pd

from v1 import models


def restaurant_orders_to_cheated_orders(
        units_restaurant_orders: Iterable[Sequence[tuple[str, pd.DataFrame]]],
        repeated_phone_number_count_threshold: int,
) -> list[models.CheatedOrders]:
    result = []
    for unit_name, grouped_df in units_restaurant_orders:
        for phone_number, grouped_by_phone_number_df in grouped_df.groupby('№ телефона'):
            if len(grouped_by_phone_number_df.index) < repeated_phone_number_count_threshold:
                continue
            cheated_orders = [
                models.CheatedOrder(
                    created_at=row[0],
                    number=row[1],
                ) for row in grouped_by_phone_number_df[['Дата и время', '№ заказа']].to_numpy()
            ]
            result.append(models.CheatedOrders(
                unit_name=unit_name,
                phone_number=phone_number,
                orders=cheated_orders
            ))
    return result
