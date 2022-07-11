from typing import Sequence, Iterable

import pandas as pd

import models
import models.dodo_is_api.orders
from utils.calculations import calculate_orders_with_phone_number_percent


def restaurant_orders_to_bonus_system_statistics(
        units_restaurant_orders: Iterable[Sequence[tuple[str, pd.DataFrame]]],
) -> list[models.dodo_is_api.orders.UnitBonusSystem]:
    result = []
    for unit_name, grouped_df in units_restaurant_orders:
        orders_with_phone_numbers_count = len(grouped_df[grouped_df['№ телефона'].notnull()].index)
        total_orders_count = len(grouped_df.index)
        orders_with_phone_numbers_percent = calculate_orders_with_phone_number_percent(
            orders_with_phone_numbers_count, total_orders_count)

        result.append(models.dodo_is_api.orders.UnitBonusSystem(
            orders_with_phone_numbers_count=orders_with_phone_numbers_count,
            orders_with_phone_numbers_percent=orders_with_phone_numbers_percent,
            total_orders_count=total_orders_count,
            unit_name=unit_name,
        ))
    return result
