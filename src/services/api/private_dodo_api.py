import uuid
from datetime import datetime
from typing import Iterable

import httpx
from pydantic import parse_obj_as

import models
from core import config
from utils import time_utils, exceptions


async def get_delivery_statistics(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime | None = None,
        to_datetime: datetime | None = None,
) -> list[models.UnitDeliveryStatistics]:
    url = 'https://api.dodois.io/dodopizza/ru/delivery/statistics/'
    response_json = await request_to_private_dodo_api(url, token, unit_uuids, from_datetime, to_datetime)
    return parse_obj_as(list[models.UnitDeliveryStatistics],
                        response_json['unitsStatistics'])


async def get_ingredient_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime,
        to_datetime: datetime,
) -> list[models.StopSalesByIngredients]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-ingredients'
    ingredient_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, from_datetime, to_datetime)
    return parse_obj_as(list[models.StopSalesByIngredients],
                        ingredient_stop_sales['stopSalesByIngredients'])


async def get_channels_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime,
        to_datetime: datetime,
) -> list[models.StopSalesBySalesChannels]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-channels'
    channels_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, from_datetime, to_datetime)
    return parse_obj_as(list[models.StopSalesBySalesChannels],
                        channels_stop_sales['stopSalesBySalesChannels'])


async def get_products_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime,
        to_datetime: datetime,
) -> list[models.StopSalesByProduct]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-products'
    products_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, from_datetime, to_datetime)
    return parse_obj_as(list[models.StopSalesByProduct],
                        products_stop_sales['stopSalesByProducts'])


async def get_production_statistics(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime | None = None,
        to_datetime: datetime | None = None,
) -> list[models.OrdersHandoverTime]:
    url = 'https://api.dodois.io/dodopizza/ru/production/orders-handover-time'
    response_json = await request_to_private_dodo_api(url, token, unit_uuids, from_datetime, to_datetime)
    return parse_obj_as(list[models.OrdersHandoverTime], response_json['ordersHandoverTime'])


async def request_to_private_dodo_api(
        url: str,
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        from_datetime: datetime | None = None,
        to_datetime: datetime | None = None,
) -> dict:
    if from_datetime is None:
        from_datetime = time_utils.get_moscow_datetime_now()
    if to_datetime is None:
        to_datetime = time_utils.get_moscow_datetime_now()
    headers = {
        'User-Agent': config.APP_USER_AGENT,
        'Authorization': f'Bearer {token}',
    }
    params = {
        'units': ','.join([i.hex for i in unit_uuids]),
        'from': from_datetime.strftime('%Y-%m-%dT00:00:00'),
        'to': to_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
    if not response.is_success:
        raise exceptions.PrivateDodoAPIError(status_code=response.status_code)
    return response.json()
