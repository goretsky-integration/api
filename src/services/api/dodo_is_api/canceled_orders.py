import asyncio
import uuid
from typing import AsyncGenerator

import httpx

import models
from services import parsers
from utils import time_utils, exceptions

__all__ = (
    'get_canceled_orders_partial',
    'get_order_by_uuid',
)


async def get_canceled_orders_partial(
        cookies: dict, period: time_utils.Period
) -> AsyncGenerator[list[models.OrderPartial], None]:
    url = 'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/PartialShiftOrders'
    params = {
        'page': 1,
        'date': period.to_datetime.date().isoformat(),
        'orderStateFilter': 'Failure',
    }
    async with httpx.AsyncClient(cookies=cookies) as client:
        while True:
            response = await client.get(url, params=params, timeout=30)
            if not response.is_success:
                raise exceptions.OrdersPartialAPIError
            orders = parsers.OrdersPartial(response.text).parse()
            yield orders
            if not orders:
                break
            params['page'] += 1


async def get_order_by_uuid(cookies: dict, order_uuid: uuid.UUID,
                            order_price: int, order_type: str) -> models.OrderByUUID:
    url = 'https://shiftmanager.dodopizza.ru/Managment/ShiftManagment/Order'
    params = {'orderUUId': order_uuid.hex}

    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params=params, timeout=30)
        if not response.is_success:
            raise exceptions.OrderByUUIDAPIError(order_uuid=order_uuid, order_price=order_price, order_type=order_type)
        return parsers.OrderByUUIDParser(response.text, order_uuid, order_price, order_type).parse()
