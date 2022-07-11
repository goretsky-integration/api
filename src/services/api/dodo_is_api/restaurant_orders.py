from typing import Iterable

import httpx
import pandas as pd
from fastapi import HTTPException, status
from pandas.core.groupby import DataFrameGroupBy

from core import config
from utils import time_utils

__all__ = (
    'get_restaurant_orders',
)


async def get_restaurant_orders(
        cookies: dict,
        unit_ids: Iterable[int | str],
        datetime_config: time_utils.Period,
) -> DataFrameGroupBy:
    """Get DataFrame with orders."""
    url = 'https://officemanager.dodopizza.ru/Reports/Orders/Get'
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, timeout=30, headers=headers, data={
            'filterType': 'OrdersFromRestaurant',
            'unitsIds': unit_ids,
            'OrderSources': 'Restaurant',
            'beginDate': datetime_config.from_datetime.strftime('%d.%m.%Y'),
            'endDate': datetime_config.to_datetime.strftime('%d.%m.%Y'),
            'orderTypes': ['Delivery', 'Pickup', 'Stationary']
        })
        if not response.is_success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return pd.read_html(response.text)[0].groupby('Отдел')
