from datetime import date, datetime

from fastapi import APIRouter, Body

import models
from services.statistics import orders
from utils import time_utils

router = APIRouter(prefix='/v1', tags=['Shift Manager'])


@router.post(
    path='/canceled-orders',
    response_model=list[models.OrderByUUID],
)
async def get_canceled_orders(
        cookies: dict = Body(),
        date: date | None = Body(None),
):
    period = time_utils.Period(date, date)
    return await orders.get_canceled_orders(cookies, period)
