import asyncio
from datetime import date
from typing import Iterable, TypeAlias

import httpx
import pandas as pd
from fastapi import HTTPException, status

import models
from core import config
from utils import exceptions, time_utils
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
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, timeout=30, headers=headers, data={
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
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params=params, timeout=30, headers=headers)
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


async def get_being_late_certificates(
        cookies: dict,
        unit_ids: Iterable[int],
        from_date: date | None = None,
        to_date: date | None = None,
) -> list[models.UnitBeingLateCertificates] | models.SingleUnitBeingLateCertificates:
    if from_date is None:
        from_date = time_utils.get_moscow_datetime_now().date()
    if to_date is None:
        to_date = time_utils.get_moscow_datetime_now().date()
    url = 'https://officemanager.dodopizza.ru/Reports/BeingLateCertificates/Get'
    data = {
        'unitsIds': tuple(unit_ids),
        'beginDate': from_date.strftime('%d.%m.%Y'),
        'endDate': to_date.strftime('%d.%m.%Y'),
    }
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, data=data, headers=headers, timeout=30)
    return parsers.BeingLateCertificatesParser(response.text).parse()
