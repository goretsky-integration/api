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
