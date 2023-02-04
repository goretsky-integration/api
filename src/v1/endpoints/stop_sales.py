import datetime

from fastapi import APIRouter, Body, Depends
from pydantic import conset

from services.external_dodo_api import OfficeManagerAPI
from services.http_client_factories import HTTPClient
from services.periods import Period
from v1.endpoints.dependencies import get_closing_office_manager_api_client
from v1.models import StopSaleBySector, StopSaleByStreet

router = APIRouter(prefix='/v1/{country_code}/stop-sales', tags=['Stop sales'])


@router.get(
    path='/sectors',
    response_model=list[StopSaleBySector],
)
async def get_stop_sales_by_sectors(
        start: datetime.datetime = Body(...),
        end: datetime.datetime = Body(...),
        unit_ids: conset(int, min_items=1, max_items=30) = Body(...),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
):
    period = Period(start, end)
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        return await api.get_stop_sales_by_sectors(period, unit_ids)


@router.get(
    path='/streets',
    response_model=list[StopSaleByStreet],
)
async def get_stop_sales_by_streets(
        start: datetime.datetime = Body(...),
        end: datetime.datetime = Body(...),
        unit_ids: conset(int, min_items=1, max_items=30) = Body(...),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
):
    period = Period(start, end)
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        return await api.get_stop_sales_by_streets(period, unit_ids)
