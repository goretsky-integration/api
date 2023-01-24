from dataclasses import dataclass
from typing import Iterable
from uuid import UUID

from pydantic import parse_obj_as

from v2 import models, exceptions
from v2.periods import Period, round_to_hours
from v2.services.http_client_factories import HTTPClient
from v2.services.private_dodo_api import stringify_uuids


@dataclass(frozen=True, slots=True)
class DodoISAPI:
    client: HTTPClient

    async def get_production_productivity_statistics(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.UnitProductivityStatistics, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:00:00'),
            'to': round_to_hours(period.end).strftime('%Y-%m-%dT%H:00:00'),
        }
        response = await self.client.get('/production/productivity', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing or not rounded to hour')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(tuple[models.UnitProductivityStatistics, ...], response.json()['productivityStatistics'])

    async def get_delivery_statistics(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.UnitDeliveryStatistics, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': period.end.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        response = await self.client.get('/delivery/statistics/', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(tuple[models.UnitDeliveryStatistics, ...], response.json()['unitsStatistics'])

    async def get_stop_sales_by_sales_channels(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.StopSaleBySalesChannels, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': period.end.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        response = await self.client.get('/production/stop-sales-channels', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(tuple[models.StopSaleBySalesChannels, ...], response.json()['stopSalesBySalesChannels'])

    async def get_stop_sales_by_ingredients(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.StopSaleByIngredients, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': period.end.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        response = await self.client.get('/production/stop-sales-ingredients', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(tuple[models.StopSaleByIngredients, ...], response.json()['stopSalesByIngredients'])

    async def get_orders_handover_time_statistics(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.OrdersHandoverTime, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'to': period.end.strftime('%Y-%m-%dT%H:%M:%S'),
        }
        response = await self.client.get('/production/orders-handover-time', params=params)
        if response.status_code == 400:
            raise exceptions.BadRequest('From or to parameter is missing')
        elif response.status_code == 401:
            raise exceptions.Unauthorized
        return parse_obj_as(tuple[models.OrdersHandoverTime, ...], response.json()['ordersHandoverTime'])

    async def get_late_delivery_vouchers(
            self,
            period: Period,
            unit_uuids: Iterable[UUID],
    ) -> tuple[models.LateDeliveryVoucher, ...]:
        params = {
            'units': stringify_uuids(unit_uuids),
            'from': period.start.strftime('%Y-%m-%dT00:00:00'),
            'to': period.end.strftime('%Y-%m-%dT00:00:00'),
            'take': 1000,
            'skip': 0,
        }
        vouchers = []
        while True:
            response = await self.client.get('/delivery/vouchers', params=params)
            response_data = response.json()
            if response_data['isEndOfListReached']:
                vouchers += response_data['vouchers']
                break
            params['skip'] = params['skip'] + 1000
        return parse_obj_as(tuple[models.LateDeliveryVoucher, ...], vouchers)
