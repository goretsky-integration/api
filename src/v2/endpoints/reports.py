from fastapi import APIRouter, Depends, Query

from v2.periods import Period
from v2.services.private_dodo_api import PrivateDodoAPI
from v2.endpoints.bearer import AccessTokenBearer
from v2.models import UnitUUIDsIn, CountryCode, UnitProductivityBalanceStatistics

router = APIRouter(prefix='/v2/{country_code}/reports', tags=['Reports'])


@router.get(
    path='/productivity-balance',
    response_model=list[UnitProductivityBalanceStatistics],
)
async def get_productivity_balance_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    # print(await api.get_production_productivity_statistics(period, unit_uuids))
    print(await api.get_delivery_statistics(period, unit_uuids))



@router.get(
    path='/total-cooking-time',
)
async def get_total_cooking_time_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/restaurant-cooking-time',
)
async def get_restaurant_cooking_time_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/kitchen-productivity',
)
async def get_kitchen_productivity_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/heated-shelf-time',
)
async def get_heated_shelf_time_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/delivery-speed',
)
async def get_delivery_speed_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/delivery-productivity',
)
async def get_delivery_productivity_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass


@router.get(
    path='/being-late-certificates',
)
async def get_being_late_certificates_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    pass
