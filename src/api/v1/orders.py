import asyncio
from typing import Iterable

from fastapi import APIRouter, Body, Depends

from api import common_schemas
from api.v1 import schemas
from api.v1.dependencies import get_closing_office_manager_api_client, get_closing_shift_manager_api_client
from services.domain.sales import restaurant_orders_to_cheated_orders
from services.external_dodo_api import OfficeManagerAPI, ShiftManagerAPI
from services.http_client_factories import HTTPClient
from services.periods import Period

router = APIRouter(prefix='/v1/{country_code}', tags=['Orders'])


@router.post(
    path='/cheated-orders',
)
async def get_cheated_orders(
        units: common_schemas.UnitIDsAndNames = Body(),
        repeated_phone_number_count_threshold: int = Body(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> list[schemas.CheatedOrders]:
    period = Period.today()
    unit_ids = [unit.id for unit in units]
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        orders = await api.get_restaurant_orders(unit_ids, period)
    return restaurant_orders_to_cheated_orders(orders, repeated_phone_number_count_threshold)


@router.get(
    path='/canceled-orders',
)
async def get_canceled_orders(
        closing_shift_manager_api_client: HTTPClient = Depends(get_closing_shift_manager_api_client),
) -> list[schemas.OrderByUUID]:
    period = Period.today()
    async with closing_shift_manager_api_client as client:
        tasks = []
        api = ShiftManagerAPI(client)
        async for orders in api.get_partial_canceled_orders(period):
            if not orders:
                break
            for order in orders:
                tasks.append(api.get_order_detail(order.uuid, order.price, order.type))
        return await asyncio.gather(*tasks)
