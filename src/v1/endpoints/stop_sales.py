import datetime

from fastapi import APIRouter, Body
from pydantic import conset

from v1.models import StopSaleBySector, StopSaleByStreet
from v1.services.stop_sales import StopSalesAPI
from v2.periods import Period

router = APIRouter(prefix='/v1/stop-sales', tags=['Stop sales'])


@router.post(
    path='/sectors',
    response_model=list[StopSaleBySector],
)
async def get_stop_sales_by_sectors(
        cookies: dict[str, str] = Body(...),
        start: datetime.datetime = Body(...),
        end: datetime.datetime = Body(...),
        unit_ids: conset(int, min_items=1, max_items=30) = Body(...),
):
    period = Period(start, end)
    api = StopSalesAPI(cookies)
    return await api.get_stop_sales_by_sectors(period, unit_ids)


@router.post(
    path='/streets',
    response_model=list[StopSaleByStreet],
)
async def get_stop_sales_by_streets(
        cookies: dict[str, str] = Body(...),
        start: datetime.datetime = Body(...),
        end: datetime.datetime = Body(...),
        unit_ids: conset(int, min_items=1, max_items=30) = Body(...),
):
    period = Period(start, end)
    api = StopSalesAPI(cookies)
    return await api.get_stop_sales_by_streets(period, unit_ids)
