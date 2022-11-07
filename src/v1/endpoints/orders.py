import asyncio
import datetime

from fastapi import APIRouter, Body

from v1.models import UnitIdsAndNamesIn, CheatedOrders, OrderByUUID
from v1.services.orders import get_restaurant_orders, restaurant_orders_to_cheated_orders, get_order_by_uuid, \
    get_canceled_orders_partial
from v2.periods import Period

router = APIRouter(prefix='/v1', tags=['Orders'])


@router.post(
    path='/cheated-orders',
    response_model=list[CheatedOrders],
)
async def get_cheated_orders(
        cookies: dict = Body(),
        units: UnitIdsAndNamesIn = Body(),
        repeated_phone_number_count_threshold: int = Body(),
):
    period = Period.today()
    unit_ids = [unit.id for unit in units]
    orders = await get_restaurant_orders(cookies, unit_ids, period)
    return restaurant_orders_to_cheated_orders(orders, repeated_phone_number_count_threshold)


@router.post(
    path='/canceled-orders',
    response_model=list[OrderByUUID],
)
async def get_canceled_orders(cookies: dict = Body(), date: datetime.date | None = Body(default=None)):
    period = Period.today()
    tasks = []
    async for orders in get_canceled_orders_partial(cookies, period):
        if not orders:
            break
        for order in orders:
            tasks.append(get_order_by_uuid(cookies, order.uuid, order.price, order.type))
    return await asyncio.gather(*tasks)
