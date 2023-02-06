import asyncio

from fastapi import APIRouter, Depends, Query
from fastapi_cache.decorator import cache

from api import common_schemas
from api.v2 import schemas, dependencies
from models.domain import delivery as delivery_models
from models.domain import production as production_models
from services.domain import delivery as delivery_services
from services.domain import production as production_services
from services.domain import sales as sales_services
from services.external_dodo_api import DodoISAPI
from services.http_client_factories import HTTPClient
from services.periods import Period

router = APIRouter(prefix='/v2/{country_code}/reports', tags=['Reports'])


@router.get(
    path='/productivity-balance',
)
@cache(expire=60, namespace='productivity-balance')
async def get_productivity_balance_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitProductivityBalanceStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        productivity_statistics, delivery_statistics, stop_sales = await asyncio.gather(
            api.get_production_productivity_statistics(period, unit_uuids),
            api.get_delivery_statistics(period, unit_uuids),
            api.get_stop_sales_by_sales_channels(period, unit_uuids),
        )
    return production_services.calculate_productivity_balance(
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
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitRestaurantCookingTimeStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        orders = await api.get_orders_handover_time_statistics(period, unit_uuids)
    return production_services.calculate_restaurant_cooking_time(unit_uuids, orders)


@router.get(
    path='/heated-shelf-time',
)
@cache(expire=60, namespace='heated-shelf-time')
async def get_heated_shelf_time_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitHeatedShelfTimeStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        production_productivity_statistics = await api.get_production_productivity_statistics(period, unit_uuids)
    return [
        production_models.UnitHeatedShelfTimeStatistics(
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
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitDeliverySpeedStatistics]:
    period = Period.today()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        units_delivery_statistics = await api.get_delivery_statistics(period, unit_uuids)
    return delivery_services.calculate_units_delivery_speed_statistics(
        all_unit_uuids=unit_uuids,
        delivery_statistics=units_delivery_statistics,
    )


@router.get(
    path='/delivery-productivity',
)
@cache(expire=60, namespace='delivery-productivity')
async def get_delivery_productivity_statistics(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitDeliveryProductivityStatistics]:
    today_period, week_before_period = Period.today(), Period.week_before_to_this_time()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        today_delivery_statistics, week_before_delivery_statistics = await asyncio.gather(
            api.get_delivery_statistics(today_period, unit_uuids),
            api.get_delivery_statistics(week_before_period, unit_uuids),
        )
    return delivery_services.calculate_delivery_productivity_statistics(
        unit_uuids=unit_uuids,
        today_delivery_statistics=today_delivery_statistics,
        week_before_delivery_statistics=week_before_delivery_statistics,
    )


@router.get(
    path='/being-late-certificates',
)
@cache(expire=60, namespace='being-late-certificates')
async def get_being_late_certificates_for_today_and_week_before(
        unit_uuids: common_schemas.UnitUUIDs = Query(),
        closing_dodo_is_api_client: HTTPClient = Depends(dependencies.get_closing_dodo_is_api_client),
) -> list[schemas.UnitBeingLateCertificatesTodayAndWeekBefore]:
    today, week_before = Period.today(), Period.week_before()
    async with closing_dodo_is_api_client as client:
        api = DodoISAPI(client)
        today_vouchers, week_before_vouchers = await asyncio.gather(
            api.get_late_delivery_vouchers(today, unit_uuids),
            api.get_late_delivery_vouchers(week_before, unit_uuids),
        )
    today_vouchers_count = delivery_services.count_late_delivery_vouchers(today_vouchers)
    week_before_vouchers_count = delivery_services.count_late_delivery_vouchers(week_before_vouchers)
    return [
        sales_services.UnitBeingLateCertificatesTodayAndWeekBefore(
            unit_uuid=unit_uuid,
            certificates_count_today=today_vouchers_count.get(unit_uuid, 0),
            certificates_count_week_before=week_before_vouchers_count.get(unit_uuid, 0),
        ) for unit_uuid in unit_uuids
    ]
