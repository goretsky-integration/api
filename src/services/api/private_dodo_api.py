import statistics
import uuid
from typing import Iterable

import httpx
from pydantic import parse_obj_as

import models
from core import config
from utils import time_utils, exceptions


async def get_delivery_statistics(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period
) -> list[models.UnitDeliveryStatistics]:
    url = 'https://api.dodois.io/dodopizza/ru/delivery/statistics/'
    response_json = await request_to_private_dodo_api(url, token, unit_uuids, datetime_config)
    return parse_obj_as(list[models.UnitDeliveryStatistics],
                        response_json['unitsStatistics'])


async def get_ingredient_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> list[models.StopSalesByIngredients]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-ingredients'
    ingredient_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, datetime_config)
    return parse_obj_as(list[models.StopSalesByIngredients],
                        ingredient_stop_sales['stopSalesByIngredients'])


async def get_channels_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> list[models.StopSalesBySalesChannels]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-channels'
    channels_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, datetime_config)
    return parse_obj_as(list[models.StopSalesBySalesChannels],
                        channels_stop_sales['stopSalesBySalesChannels'])


async def get_products_stop_sales(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> list[models.StopSalesByProduct]:
    url = 'https://api.dodois.io/dodopizza/ru/production/stop-sales-products'
    products_stop_sales = await request_to_private_dodo_api(url, token, unit_uuids, datetime_config)
    return parse_obj_as(list[models.StopSalesByProduct],
                        products_stop_sales['stopSalesByProducts'])


async def get_orders_handover_time(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> list[models.OrdersHandoverTime]:
    url = 'https://api.dodois.io/dodopizza/ru/production/orders-handover-time'
    response_json = await request_to_private_dodo_api(url, token, unit_uuids, datetime_config)
    return parse_obj_as(list[models.OrdersHandoverTime], response_json['ordersHandoverTime'])


async def request_to_private_dodo_api(
        url: str,
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> dict:
    headers = {
        'User-Agent': config.APP_USER_AGENT,
        'Authorization': f'Bearer {token}',
    }
    params = {
        'units': ','.join([i.hex for i in unit_uuids]),
        'from': datetime_config.from_datetime.strftime('%Y-%m-%dT00:00:00'),
        'to': datetime_config.to_datetime.strftime('%Y-%m-%dT%H:%M:%S'),
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params, headers=headers)
    if not response.is_success:
        raise exceptions.PrivateDodoAPIError(status_code=response.status_code)
    return response.json()


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(get_orders_handover_time('103C7E11CA808AF59E5ABDAE445399560D578BCFDF6A818A4DFD59B1267CF2F5',
                                               [uuid.UUID('000d3a24-0c71-9a87-11e6-8aba13f80da9'),
                                                uuid.UUID('000d3a24-0c71-9a87-11e6-8aba13f82835'),
                                                uuid.UUID('000d3a24-0c71-9a87-11e6-8aba13f88754')],
    time_utils.Period.new_today())))
