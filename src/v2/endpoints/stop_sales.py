import datetime

from fastapi import APIRouter, Depends, Query

from v2.models import StopSaleBySalesChannels, CountryCode, UnitUUIDsIn, StopSaleByIngredients
from v2.endpoints.bearer import AccessTokenBearer
from v2.periods import Period
from v2.services.private_dodo_api import PrivateDodoAPI

router = APIRouter(prefix='/v2/{country_code}/stop-sales', tags=['Stop sales'])


@router.get(
    path='/channels',
    response_model=list[StopSaleBySalesChannels],
    response_model_by_alias=False,
)
async def get_stop_sales_by_sales_channels(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        start: datetime.datetime = Query(),
        end: datetime.datetime = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period(start, end)
    api = PrivateDodoAPI(token, country_code)
    return await api.get_stop_sales_by_sales_channels(period, unit_uuids)


@router.get(
    path='/ingredients',
    response_model=list[StopSaleByIngredients],
    response_model_by_alias=False,
)
async def get_stop_sales_by_ingredients(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        start: datetime.datetime = Query(),
        end: datetime.datetime = Query(),
        token: str = Depends(AccessTokenBearer()),

):
    period = Period(start, end)
    api = PrivateDodoAPI(token, country_code)
    return await api.get_stop_sales_by_ingredients(period, unit_uuids)
