from typing import Iterable

import httpx
import pandas as pd

__all__ = (
    'get_restaurant_orders',
)

from fastapi import HTTPException

from starlette import status


async def get_restaurant_orders(
        cookies: dict,
        unit_ids: Iterable[int | str], date: str
) -> pd.DataFrame:
    """Get DataFrame with orders."""
    url = 'https://officemanager.dodopizza.ru/Reports/Orders/Get'
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, timeout=30, data={
            'filterType': 'OrdersFromRestaurant',
            'unitsIds': unit_ids,
            'OrderSources': 'Restaurant',
            'beginDate': date,
            'endDate': date,
            'orderTypes': ['Delivery', 'Pickup', 'Stationary']
        })
        if not response.is_success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return pd.read_html(response.text)[0]
