from datetime import date

from fastapi import APIRouter, Body

import models
from services import convert_models
from services.statistics import orders
from utils import time_utils

router = APIRouter(prefix='/v1', tags=['Orders'])


@router.post(
    path='/cheated-orders',
    response_model=list[models.CheatedOrders],
)
async def get_canceled_orders(
        cookies: dict = Body(...),
        units: list[models.UnitIdAndName] = Body(...),
        date: date | None = Body(None),
        repeated_phone_number_count_threshold: int = Body(3),
):
    period = time_utils.Period(date, date)
    restaurant_orders = await orders.get_restaurant_orders(cookies, units, period)
    return convert_models.restaurant_orders_to_cheated_orders(restaurant_orders, repeated_phone_number_count_threshold)
