from enum import Enum
from typing import Iterable, Any

import pandas as pd

import models
from utils.calculations import calculate_orders_percentage_with_phone_numbers


class ColumnName(str, Enum):
    DEPARTMENT = 'Отдел'
    PHONE_NUMBER = '№ телефона'
    DATETIME = 'Дата и время'
    ORDER_NUMBER = '№ заказа'


def get_rows_with_phone_number(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe[ColumnName.PHONE_NUMBER].notnull()]


def count_rows_with_phone_number(dataframe: pd.DataFrame) -> int:
    return count_rows_amount(get_rows_with_phone_number(dataframe))


def group_by_department(dataframe: pd.DataFrame) -> Iterable[tuple[str, pd.DataFrame]]:
    """
    Args:
        dataframe: Dataframe need to be grouped.

    Returns:
        Iterable of tuples.
        Each tuple contains name of department dataframe grouped by
        and grouped part of dataframe.
    """
    return dataframe.groupby([ColumnName.DEPARTMENT])


def count_rows_amount(series: pd.DataFrame | pd.Series) -> int:
    return len(series.index)


def is_series_empty(series: pd.Series) -> bool:
    return count_rows_amount(series) == 0


def count_phone_numbers(dataframe: pd.DataFrame) -> pd.Series:
    return dataframe[ColumnName.PHONE_NUMBER].value_counts()


def filter_by_column(dataframe: pd.DataFrame, column_name: ColumnName, value: Any) -> pd.DataFrame:
    return dataframe[dataframe[column_name] == value]


def filter_by_phone_number(dataframe: pd.DataFrame, value: Any) -> pd.DataFrame:
    return filter_by_column(dataframe, ColumnName.PHONE_NUMBER, value)


def extract_column_values(dataframe: pd.DataFrame, column_name: ColumnName) -> pd.Series:
    return dataframe[column_name].values


def get_cheated_orders(dataframe: pd.DataFrame) -> list[models.CheatedOrder]:
    datetimes = extract_column_values(dataframe, ColumnName.DATETIME)
    order_numbers = extract_column_values(dataframe, ColumnName.ORDER_NUMBER)
    return [models.CheatedOrder(cheated_at=dt, no=no)
            for dt, no in zip(datetimes, order_numbers)]


def parse_restaurant_orders_dataframe(orders_dataframe: pd.DataFrame) -> list[models.RestaurantOrdersStatistics]:
    result = []
    for department_name, department_orders in group_by_department(orders_dataframe):
        phone_numbers_amount = count_rows_with_phone_number(department_orders)
        total_orders_amount = count_rows_amount(department_orders)
        result.append(models.RestaurantOrdersStatistics(
            department=department_name,
            orders_with_phone_numbers_amount=phone_numbers_amount,
            total_orders_amount=total_orders_amount,
            orders_with_phone_numbers_percentage=calculate_orders_percentage_with_phone_numbers(
                phone_numbers_amount, total_orders_amount
            ),
        ))
    return result
