from typing import Iterable, Sequence

import pandas as pd

from models.domain import sales as sales_models
from models.external_api_responses import public_api as publib_api_models

__all__ = (
    'calculate_total_revenue',
    'calculate_units_revenue',
    'calculate_percent_from_week_before',
    'restaurant_orders_to_cheated_orders'
)


def calculate_percent_from_week_before(now: int, week_before: int) -> int:
    if week_before == 0:
        return 0
    return round(now / week_before * 100) - 100


def calculate_units_revenue(
        units: Iterable[publib_api_models.UnitOperationalStatisticsForTodayAndWeekBefore],
) -> list[sales_models.UnitRevenue]:
    return [
        sales_models.UnitRevenue(
            unit_id=unit.unit_id,
            today=unit.today.revenue,
            from_week_before_in_percents=calculate_percent_from_week_before(
                now=unit.today.revenue,
                week_before=unit.week_before_to_this_time.revenue,
            )
        ) for unit in units
    ]


def calculate_total_revenue(
        units: Iterable[publib_api_models.UnitOperationalStatisticsForTodayAndWeekBefore],
) -> sales_models.TotalRevenue:
    total_revenue_today = sum(unit.today.revenue for unit in units)
    total_revenue_week_before = sum(unit.week_before_to_this_time.revenue for unit in units)
    from_week_before_in_percents = calculate_percent_from_week_before(total_revenue_today, total_revenue_week_before)
    return sales_models.TotalRevenue(
        today=total_revenue_today,
        from_week_before_in_percents=from_week_before_in_percents,
    )


def restaurant_orders_to_cheated_orders(
        units_restaurant_orders: Iterable[Sequence[tuple[str, pd.DataFrame]]],
        repeated_phone_number_count_threshold: int,
) -> list[sales_models.CheatedOrders]:
    result = []
    for unit_name, grouped_df in units_restaurant_orders:
        for phone_number, grouped_by_phone_number_df in grouped_df.groupby('№ телефона'):
            if len(grouped_by_phone_number_df.index) < repeated_phone_number_count_threshold:
                continue
            cheated_orders = [
                sales_models.CheatedOrder(
                    created_at=row[0],
                    number=row[1],
                ) for row in grouped_by_phone_number_df[['Дата и время', '№ заказа']].to_numpy()
            ]
            result.append(sales_models.CheatedOrders(
                unit_name=unit_name,
                phone_number=phone_number,
                orders=cheated_orders
            ))
    return result
