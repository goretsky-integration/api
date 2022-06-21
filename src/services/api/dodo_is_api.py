from typing import Iterable

import httpx
import pandas as pd
from fastapi import HTTPException, status

import models
from services import parsers

__all__ = (
    'get_restaurant_orders',
    'get_kitchen_statistics',
)


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


async def get_kitchen_statistics(
        cookies: dict,
        unit_id: int | str,
) -> models.KitchenStatistics:
    url = 'https://officemanager.dodopizza.ru/OfficeManager/OperationalStatistics/KitchenPartial'
    params = {'unitId': unit_id}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params=params, timeout=30)
        if not response.is_success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return parsers.KitchenStatisticsParser(response.text, unit_id).parse()
