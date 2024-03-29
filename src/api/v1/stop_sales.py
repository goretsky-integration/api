from fastapi import APIRouter, Depends, Query
from pydantic import conset

from api import common_schemas
from api.v1 import schemas, dependencies
from services.external_dodo_api import OfficeManagerAPI
from services.http_client_factories import AsyncHTTPClient
from services.periods import Period

router = APIRouter(prefix='/v1/{country_code}/stop-sales', tags=['Stop sales'])


@router.get(
    path='/sectors',
)
async def get_stop_sales_by_sectors(
        unit_ids: common_schemas.UnitIDs = Query(),
        period: Period = Depends(Period),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> list[schemas.StopSaleBySector]:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        return await api.get_stop_sales_by_sectors(period, unit_ids)


@router.get(
    path='/streets',
)
async def get_stop_sales_by_streets(
        unit_ids: conset(int, min_items=1, max_items=30) = Query(...),
        period: Period = Depends(Period),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> list[schemas.StopSaleByStreet]:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        return await api.get_stop_sales_by_streets(period, unit_ids)
