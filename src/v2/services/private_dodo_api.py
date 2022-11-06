import contextlib
import uuid
from typing import Iterable

import httpx
from pydantic import parse_obj_as

from core import config
from v2 import models
from v2 import exceptions
from v2.periods import Period


def stringify_uuids(uuids: Iterable[uuid.UUID]) -> str:
    return ','.join((uuid_item.hex for uuid_item in uuids))


class PrivateDodoAPI:

    def __init__(self, token: str, country_code: str):
        self._token = token
        self._country_code = country_code

    @property
    def base_url(self) -> str:
        return f'https://api.dodois.io/dodopizza/{self._country_code}/'

    @property
    def headers(self) -> dict:
        return {
            'User-Agent': config.APP_USER_AGENT,
            'Authorization': f'Bearer {self._token}',
        }

    @contextlib.asynccontextmanager
    async def get_api_client(self) -> httpx.AsyncClient:
        async with httpx.AsyncClient(base_url=self.base_url, headers=self.headers) as client:
            yield client

    async def get_production_productivity_statistics(
            self,
            period: Period,
            unit_uuids: Iterable[uuid.UUID],
    ) -> list[models.UnitProductivityStatistics]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:00:00'),
            'to': period.end.strftime('%Y-%m-%dT%H:00:00'),
        }
        async with self.get_api_client() as client:
            response = await client.get('/production/productivity', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing or not rounded to hour')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(list[models.UnitProductivityStatistics], response.json()['productivityStatistics'])

    async def get_delivery_statistics(
            self,
            period: Period,
            unit_uuids: Iterable[uuid.UUID],
    ) -> list[models.UnitDeliveryStatistics]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': period.end.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        async with self.get_api_client() as client:
            response = await client.get('/delivery/statistics/', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(list[models.UnitDeliveryStatistics], response.json()['unitsStatistics'])

