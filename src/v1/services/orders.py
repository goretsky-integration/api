import uuid
from typing import Iterable, Sequence, AsyncGenerator

import httpx
import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from core import config
from v1 import models, parsers
from v2.periods import Period


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


async def get_restaurant_orders(
        cookies: dict,
        unit_ids: Iterable[int | str],
        period: Period,
) -> DataFrameGroupBy:
    """Get DataFrame with orders."""
    url = 'https://officemanager.dodopizza.ru/Reports/Orders/Get'
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, timeout=30, headers=headers, data={
            'filterType': 'OrdersFromRestaurant',
            'unitsIds': tuple(unit_ids),
            'OrderSources': 'Restaurant',
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
            'orderTypes': ['Delivery', 'Pickup', 'Stationary']
        })
        return pd.read_html(response.text)[0].groupby('Отдел')


async def get_canceled_orders_partial(
        cookies: dict, period: Period
) -> AsyncGenerator[list[models.OrderPartial], None]:
    url = 'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/PartialShiftOrders'
    params = {
        'page': 1,
        'date': period.end.date().isoformat(),
        'orderStateFilter': 'Failure',
    }
    async with httpx.AsyncClient(cookies=cookies) as client:
        while True:
            response = await client.get(url, params=params, timeout=30)
            orders = parsers.OrdersPartial(response.text).parse()
            yield orders
            if not orders:
                break
            params['page'] += 1


async def get_order_by_uuid(cookies: dict, order_uuid: uuid.UUID,
                            order_price: int, order_type: str) -> models.OrderByUUID:
    url = 'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Order'
    params = {'orderUUId': order_uuid.hex}

    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params=params, timeout=30)
        if not response.is_success:
            raise exceptions.OrderByUUIDAPIError(order_uuid=order_uuid, order_price=order_price, order_type=order_type)
        return parsers.OrderByUUIDParser(response.text, order_uuid, order_price, order_type).parse()
