import asyncio
import datetime
import statistics
import uuid
from typing import Iterable

from fastapi import APIRouter, Depends, Query

from v2 import models
from v2.endpoints.bearer import AccessTokenBearer
from v2.models import UnitUUIDsIn, CountryCode, UnitProductivityBalanceStatistics
from v2.periods import Period
from v2.services import production_statistics, delivery_statistics
from v2.services.private_dodo_api import PrivateDodoAPI

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
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    orders = await api.get_orders_handover_time_statistics(period, unit_uuids)
    print(orders)
    a = statistics.mean([order.tracking_pending_time for order in orders])
    b = statistics.mean([order.cooking_time for order in orders])
    c = statistics.mean(
        [order.heated_shelf_time for order in orders if order.sales_channel.name != models.SalesChannel.DELIVERY.name])
    print(a + b + c)


@router.get(
    path='/restaurant-cooking-time',
    response_model=list[models.UnitRestaurantCookingTimeStatistics],
)
async def get_restaurant_cooking_time_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    orders = await api.get_orders_handover_time_statistics(period, unit_uuids)
    unit_uuid_to_orders = production_statistics.group_by_unit_uuids(orders)
    return [production_statistics.orders_to_restaurant_cooking_time_dto(unit_uuid, unit_uuid_to_orders[unit_uuid])
            for unit_uuid in unit_uuids]


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
    response_model=list[models.UnitHeatedShelfTimeStatistics],
)
async def get_heated_shelf_time_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    production_productivity_statistics = await api.get_production_productivity_statistics(period, unit_uuids)
    return [
        models.UnitHeatedShelfTimeStatistics(
            unit_uuid=unit.unit_uuid,
            average_heated_shelf_time=unit.avg_heated_shelf_time,
        ) for unit in production_productivity_statistics
    ]


@router.get(
    path='/delivery-speed',
    response_model=list[models.UnitDeliverySpeedStatistics],
)
async def get_delivery_speed_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    units_delivery_statistics = await api.get_delivery_statistics(period, unit_uuids)
    unit_uuids_from_api = {unit.unit_uuid for unit in units_delivery_statistics}
    unit_uuids_not_from_api = unit_uuids - unit_uuids_from_api
    empty_delivery_statistics = [models.UnitDeliverySpeedStatistics(unit_uuid=unit_uuid) for unit_uuid in
                                 unit_uuids_not_from_api]
    return [delivery_statistics.delivery_statistics_to_delivery_speed(unit_delivery_statistics)
            for unit_delivery_statistics in units_delivery_statistics] + empty_delivery_statistics


@router.get(
    path='/delivery-productivity',
)
async def get_delivery_productivity_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    today_period = Period.today()
    week_before_period = Period.week_ago()
    api = PrivateDodoAPI(token, country_code)
    today_units_delivery_statistics, week_before_units_delivery_statistics = await asyncio.gather(
        api.get_delivery_statistics(today_period, unit_uuids),
        api.get_delivery_statistics(week_before_period, unit_uuids),
    )
    unit_uuid_to_today_statistics = {unit.unit_uuid: unit for unit in today_units_delivery_statistics}
    unit_uuid_to_week_before_statistics = {unit.unit_uuid: unit for unit in week_before_units_delivery_statistics}
    return [
        delivery_statistics.to_today_and_week_before_delivery_productivity(
            unit_uuid=unit_uuid,
            unit_today_delivery_statistics=unit_uuid_to_today_statistics[unit_uuid],
            unit_week_delivery_statistics=unit_uuid_to_week_before_statistics[unit_uuid],
        ) for unit_uuid in unit_uuids
    ]
