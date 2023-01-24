from fastapi import APIRouter, Depends, Query

from v2.endpoints.dependencies import get_closing_dodo_is_api_client_factory, get_period
from v2.models import StopSaleBySalesChannels, UnitUUIDsIn, StopSaleByIngredients
from v2.periods import Period
from v2.services.external_dodo_api import DodoISAPI
from v2.services.http_client_factories import HTTPClient

router = APIRouter(prefix='/v2/{country_code}/stop-sales', tags=['Stop sales'])


@router.get(
    path='/channels',
    response_model=list[StopSaleBySalesChannels],
    response_model_by_alias=False,
)
async def get_stop_sales_by_sales_channels(
        closing_dodo_is_api_client_factory: HTTPClient = Depends(get_closing_dodo_is_api_client_factory),
        unit_uuids: UnitUUIDsIn = Query(),
        period: Period = Depends(get_period),
):
    async with closing_dodo_is_api_client_factory as client:
        api = DodoISAPI(client)
        return api.get_stop_sales_by_sales_channels(period, unit_uuids)


@router.get(
    path='/ingredients',
    response_model=list[StopSaleByIngredients],
    response_model_by_alias=False,
)
async def get_stop_sales_by_ingredients(
        closing_dodo_is_api_client_factory: HTTPClient = Depends(get_closing_dodo_is_api_client_factory),
        unit_uuids: UnitUUIDsIn = Query(),
        period: Period = Depends(get_period),
):
    async with closing_dodo_is_api_client_factory as client:
        api = DodoISAPI(client)
        return api.get_stop_sales_by_ingredients(period, unit_uuids)
