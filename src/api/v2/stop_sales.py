from typing import Iterable

from fastapi import APIRouter, Depends, Query

from api import common_schemas
from api.v2 import schemas
from api.v2.dependencies import get_closing_dodo_is_api_client
from services.external_dodo_api import DodoISAPI
from services.http_client_factories import HTTPClient
from services.periods import Period

router = APIRouter(prefix='/v2/{country_code}/stop-sales', tags=['Stop sales'])


@router.get(
    path='/channels',
    response_model_by_alias=False,
)
async def get_stop_sales_by_sales_channels(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        period: Period = Depends(Period),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> Iterable[schemas.StopSaleBySalesChannels]:
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        return await api.get_stop_sales_by_sales_channels(period, unit_uuids)


@router.get(
    path='/ingredients',
    response_model_by_alias=False,
)
async def get_stop_sales_by_ingredients(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        period: Period = Depends(Period),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> Iterable[schemas.StopSaleByIngredients]:
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        return await api.get_stop_sales_by_ingredients(period, unit_uuids)
