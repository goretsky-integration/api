import uuid
from datetime import datetime

from fastapi import APIRouter, Query, Body

import models
from services.api import dodo_is_api
from utils import time_utils

router = APIRouter(prefix='/v1/stop-sales', tags=['Stop sales'])


@router.post(
    path='/sectors',
    response_model=list[models.StopSalesBySector],
)
async def get_sectors_stop_sales(
        cookies: dict,
        unit_ids: set[int] = Body(...),
        from_datetime: datetime | None = Body(None, description='Today unless specified'),
        to_datetime: datetime | None = Body(None, description='Current datetime unless specified'),
):
    period = time_utils.Period(from_datetime, to_datetime)
    return await dodo_is_api.get_sector_stop_sales(cookies, unit_ids, period)


@router.post(
    path='/streets',
    response_model=list[models.StopSalesByStreet],
)
async def get_streets_stop_sales(
        cookies: dict,
        unit_ids: set[int] = Body(...),
        from_datetime: datetime | None = Body(None, description='Today unless specified'),
        to_datetime: datetime | None = Body(None, description='Current datetime unless specified'),
):
    period = time_utils.Period(from_datetime, to_datetime)
    return await dodo_is_api.get_street_stop_sales(cookies, unit_ids, period)
