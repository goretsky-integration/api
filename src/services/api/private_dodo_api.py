import uuid
from typing import Iterable

import httpx
from pydantic import parse_obj_as

import models
from core import config
from utils import time_utils


async def get_delivery_statistics(
        token: str,
        unit_uuids: Iterable[uuid.UUID]
) -> list[models.UnitDeliveryStatistics]:
    headers = {
        'User-Agent': config.APP_USER_AGENT,
        'Authorization': f'Bearer {token}',
    }
    params = {
        'units': ','.join([i.hex for i in unit_uuids]),
        'from': time_utils.get_moscow_datetime_now().strftime('%Y-%m-%dT00:00:00'),
        'to': time_utils.get_moscow_datetime_now().strftime('%Y-%m-%dT%H:%M:%S'),
    }
    url = 'https://api.dodois.io/dodopizza/ru/delivery/statistics/'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
    if not response.is_success:
        raise
    return parse_obj_as(list[models.UnitDeliveryStatistics],
                        response.json()['unitsStatistics'])
