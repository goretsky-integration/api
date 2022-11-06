import asyncio
import datetime
import uuid
from typing import Iterable

from fastapi import APIRouter, Depends, Query

from v2 import models
from v2.periods import Period
from v2.services.private_dodo_api import PrivateDodoAPI
from v2.endpoints.bearer import AccessTokenBearer
from v2.models import UnitUUIDsIn, CountryCode, UnitProductivityBalanceStatistics

router = APIRouter(prefix='/v2/{country_code}/reports', tags=['Reports'])


def zip_by_unit_uuid(
        unit_uuids: Iterable[uuid.UUID],
        productivity_statistics: Iterable[models.UnitProductivityStatistics],
        delivery_statistics: Iterable[models.UnitDeliveryStatistics],
        stop_sales: Iterable[models.StopSaleBySalesChannels],
) -> list[dict]:
    unit_uuid_to_productivity_statistics = {unit.unit_uuid: unit for unit in productivity_statistics}
    unit_uuid_to_delivery_statistics = {unit.unit_uuid: unit for unit in delivery_statistics}
    unit_uuid_to_stop_sales = {unit.unit_uuid: unit for unit in stop_sales}
    result = []
    for unit_uuid in unit_uuids:
        result.append({
            'productivity_statistics': unit_uuid_to_productivity_statistics[unit_uuid],
            'delivery_statistics': unit_uuid_to_delivery_statistics[unit_uuid],
            'stop_sales': unit_uuid_to_stop_sales[unit_uuid],
        })
    return result




@router.get(
    path='/productivity-balance',
    response_model=list[UnitProductivityBalanceStatistics],
)
async def get_productivity_balance_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period(start=datetime.datetime(2022, 10, 25), end=Period.today().end)
    api = PrivateDodoAPI(token, country_code)
    productivity_statistics, delivery_statistics, stop_sales = await asyncio.gather(
        api.get_production_productivity_statistics(period, unit_uuids),
        api.get_delivery_statistics(period, unit_uuids),
        api.get_stop_sales_by_sales_channels(period, unit_uuids),
    )
    zipped = zip_by_unit_uuid(unit_uuids, productivity_statistics, delivery_statistics, stop_sales)
    print(zipped)


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
