import asyncio
import collections
import uuid
from typing import Iterable

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from api import common_schemas
from api.v2 import schemas
from api.v2.dependencies import get_closing_dodo_is_api_client
from api.v2.schemas import UnitBeingLateCertificatesTodayAndWeekBefore
from models.domain.delivery import UnitDeliverySpeedStatistics, UnitDeliveryProductivityStatistics
from models.domain.production import UnitProductivityBalanceStatistics, UnitHeatedShelfTimeStatistics
from models.external_api_responses.dodo_is_api import (
    UnitProductivityStatistics,
    UnitDeliveryStatistics,
    StopSaleBySalesChannels, SalesChannel,
)
from models.external_api_responses.dodo_is_api.production import ChannelStopType
from services.domain.delivery import (
    delivery_statistics_to_delivery_speed,
    to_today_and_week_before_delivery_productivity,
    count_late_delivery_vouchers,
)
from services.domain.production import (
    remove_duplicated_orders,
    group_by_unit_uuids,
    orders_to_restaurant_cooking_time_dto, calculate_productivity_balance,
)
from services.external_dodo_api import DodoISAPI
from services.http_client_factories import HTTPClient
from services.periods import Period

router = APIRouter(prefix='/v2/{country_code}/reports', tags=['Reports'])


def zip_by_unit_uuid(
        unit_uuids: Iterable[uuid.UUID],
        productivity_statistics: Iterable[UnitProductivityStatistics],
        delivery_statistics: Iterable[UnitDeliveryStatistics],
        stop_sales: Iterable[StopSaleBySalesChannels],
) -> list[dict]:
    unit_uuid_to_productivity_statistics = {unit.unit_uuid: unit for unit in productivity_statistics}
    unit_uuid_to_delivery_statistics = {unit.unit_uuid: unit for unit in delivery_statistics}
    unit_uuid_to_stop_sales = {unit.unit_uuid: unit for unit in stop_sales}
    result = []
    for unit_uuid in unit_uuids:
        result.append({
            'unit_uuid': unit_uuid,
            'productivity_statistics': unit_uuid_to_productivity_statistics[unit_uuid],
            'delivery_statistics': unit_uuid_to_delivery_statistics[unit_uuid],
            'stop_sales': unit_uuid_to_stop_sales[unit_uuid],
        })
    return result


@router.get(
    path='/productivity-balance',
)
@cache(expire=60, namespace='productivity-balance')
async def get_productivity_balance_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitProductivityBalanceStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        productivity_statistics, delivery_statistics, stop_sales = await asyncio.gather(
            api.get_production_productivity_statistics(period, unit_uuids),
            api.get_delivery_statistics(period, unit_uuids),
            api.get_stop_sales_by_sales_channels(period, unit_uuids),
        )
    return calculate_productivity_balance(
        unit_uuids=unit_uuids,
        productivity_statistics=productivity_statistics,
        delivery_statistics=delivery_statistics,
        stop_sales=stop_sales,
        now=period.end,
    )


@router.get(
    path='/restaurant-cooking-time',
)
@cache(expire=60, namespace='restaurant-cooking-time')
async def get_restaurant_cooking_time_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitRestaurantCookingTimeStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        orders = await api.get_orders_handover_time_statistics(period, unit_uuids)
    unique_orders = remove_duplicated_orders(orders)
    unit_uuid_to_orders = group_by_unit_uuids(unique_orders)
    return [orders_to_restaurant_cooking_time_dto(unit_uuid, unit_uuid_to_orders[unit_uuid])
            for unit_uuid in unit_uuids]


@router.get(
    path='/heated-shelf-time',
)
@cache(expire=60, namespace='heated-shelf-time')
async def get_heated_shelf_time_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitHeatedShelfTimeStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        production_productivity_statistics = await api.get_production_productivity_statistics(period, unit_uuids)
    return [
        UnitHeatedShelfTimeStatistics(
            unit_uuid=unit.unit_uuid,
            average_heated_shelf_time=unit.avg_heated_shelf_time,
        ) for unit in production_productivity_statistics
    ]


@router.get(
    path='/delivery-speed',
)
@cache(expire=60, namespace='delivery-speed')
async def get_delivery_speed_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitDeliverySpeedStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        units_delivery_statistics = await api.get_delivery_statistics(period, unit_uuids)
    unit_uuids_from_api = {unit.unit_uuid for unit in units_delivery_statistics}
    unit_uuids_not_from_api = unit_uuids - unit_uuids_from_api
    empty_delivery_statistics = [UnitDeliverySpeedStatistics(unit_uuid=unit_uuid) for unit_uuid in
                                 unit_uuids_not_from_api]
    return [delivery_statistics_to_delivery_speed(unit_delivery_statistics)
            for unit_delivery_statistics in units_delivery_statistics] + empty_delivery_statistics


@router.get(
    path='/delivery-productivity',
)
@cache(expire=60, namespace='delivery-productivity')
async def get_delivery_productivity_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitDeliveryProductivityStatistics]:
    today_period = Period.today()
    week_before_period = Period.week_before_to_this_time()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        today_units_delivery_statistics, week_before_units_delivery_statistics = await asyncio.gather(
            api.get_delivery_statistics(today_period, unit_uuids),
            api.get_delivery_statistics(week_before_period, unit_uuids),
        )
    unit_uuid_to_today_statistics = {unit.unit_uuid: unit for unit in today_units_delivery_statistics}
    unit_uuid_to_week_before_statistics = {unit.unit_uuid: unit for unit in week_before_units_delivery_statistics}
    response = []
    for unit_uuid in unit_uuids:
        try:
            unit_today_delivery_statistics = unit_uuid_to_today_statistics[unit_uuid]
            unit_week_delivery_statistics = unit_uuid_to_week_before_statistics[unit_uuid]
        except KeyError:
            response.append(UnitDeliveryProductivityStatistics(unit_uuid=unit_uuid))
        else:
            response.append(to_today_and_week_before_delivery_productivity(
                unit_uuid,
                unit_today_delivery_statistics,
                unit_week_delivery_statistics,
            ))
    return response


@router.get(
    path='/being-late-certificates',
)
@cache(expire=60, namespace='being-late-certificates')
async def get_being_late_certificates_for_today_and_week_before(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(get_closing_dodo_is_api_client),
) -> list[schemas.UnitBeingLateCertificatesTodayAndWeekBefore]:
    today, week_before = Period.today(), Period.week_before()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        today_vouchers, week_before_vouchers = await asyncio.gather(
            api.get_late_delivery_vouchers(today, unit_uuids),
            api.get_late_delivery_vouchers(week_before, unit_uuids),
        )
    today_vouchers_count = count_late_delivery_vouchers(today_vouchers)
    week_before_vouchers_count = count_late_delivery_vouchers(week_before_vouchers)
    return [
        UnitBeingLateCertificatesTodayAndWeekBefore(
            unit_uuid=unit_uuid,
            certificates_count_today=today_vouchers_count.get(unit_uuid, 0),
            certificates_count_week_before=week_before_vouchers_count.get(unit_uuid, 0),
        ) for unit_uuid in unit_uuids
    ]
