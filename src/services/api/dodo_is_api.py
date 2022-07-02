import asyncio
from typing import Iterable, TypeAlias

import httpx
import pandas as pd
from fastapi import HTTPException, status

import models
from utils import exceptions
from services import parsers

__all__ = (
    'get_restaurant_orders',
    'get_kitchen_statistics',
)

KitchenStatisticsAPIResponse: TypeAlias = tuple[models.KitchenStatistics | exceptions.KitchenStatisticsError]


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
            raise exceptions.KitchenStatisticsError(unit_id=unit_id)
        return parsers.KitchenStatisticsParser(response.text, unit_id).parse()


async def get_kitchen_statistics_batch(
        cookies: dict,
        unit_ids: Iterable[int | str],
) -> models.KitchenStatisticsBatch:
    tasks = (get_kitchen_statistics(cookies, unit_id) for unit_id in unit_ids)
    responses: tuple[KitchenStatisticsAPIResponse, ...] = await asyncio.gather(*tasks, return_exceptions=True)
    return models.KitchenStatisticsBatch(
        kitchen_statistics=[
            response for response in responses
            if isinstance(response, models.KitchenStatistics)
        ],
        error_unit_ids=[
            response for response in responses
            if isinstance(response, exceptions.KitchenStatisticsError)
        ]
    )
