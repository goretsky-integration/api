import asyncio
import tempfile

import httpx
from fastapi import APIRouter, Query, Body, Depends
from fastapi_cache.decorator import cache

from core import config
from services.http_client_factories import HTTPClient
from v1 import exceptions, models
from v1.endpoints.dependencies import get_closing_public_api_client
from v1.models import RevenueStatisticsReport, UnitsRevenueStatistics, UnitIDsIn, \
    DeliveryPartialStatisticsReport, UnitDeliveryPartialStatistics, KitchenPartialStatisticsReport, \
    UnitKitchenPartialStatistics, UnitBonusSystemStatistics, UnitIdsAndNamesIn
from v1.parsers import DeliveryStatisticsExcelParser
from v1.services import operational_statistics
from v1.services.delivery import get_delivery_statistics_excel
from v1.services.external_dodo_api import DodoPublicAPI, get_operational_statistics_for_today_and_week_before_batch
from v1.services.operational_statistics import calculate_units_revenue, calculate_total_revenue
from v1.services.orders import get_restaurant_orders
from v2.periods import Period

router = APIRouter(tags=['Reports'])


@router.get(
    path='/v1/{country_code}/reports/revenue',
    response_model=RevenueStatisticsReport,
)
@cache(expire=60, namespace='revenue')
async def get_revenue_statistics(
        closing_public_api_client: HTTPClient = Depends(get_closing_public_api_client),
        unit_ids: UnitIDsIn = Query(),
):
    async with closing_public_api_client as client:
        api = DodoPublicAPI(client)
        units_statistics = await get_operational_statistics_for_today_and_week_before_batch(
            dodo_public_api=api, unit_ids=unit_ids
        )
    units_revenue = calculate_units_revenue(units_statistics.results)
    total_revenue = calculate_total_revenue(units_statistics.results)
    return RevenueStatisticsReport(
        results=UnitsRevenueStatistics(units=units_revenue, total=total_revenue),
        errors=units_statistics.errors,
    )


@router.post(
    path='/v1/reports/awaiting-orders',
    response_model=DeliveryPartialStatisticsReport,
)
@cache(expire=60, namespace='awaiting-orders')
async def get_delivery_partial_statistics(unit_ids: UnitIDsIn, cookies: dict = Body()):
    async with httpx.AsyncClient(cookies=cookies, headers={'User-Agent': config.APP_USER_AGENT}) as client:
        tasks = (operational_statistics.get_delivery_partial_statistics(client, unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    delivery_partial_statistics = [result for result in results if isinstance(result, UnitDeliveryPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return DeliveryPartialStatisticsReport(results=delivery_partial_statistics, errors=errors)


@router.post(
    path='/v1/reports/kitchen-productivity',
    response_model=KitchenPartialStatisticsReport,
)
@cache(expire=60, namespace='kitchen-productivity')
async def get_kitchen_partial_statistics(unit_ids: UnitIDsIn, cookies: dict = Body()):
    async with httpx.AsyncClient(cookies=cookies, headers={'User-Agent': config.APP_USER_AGENT}) as client:
        tasks = (operational_statistics.get_kitchen_partial_statistics(client, unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    kitchen_partial_statistics = [result for result in results if isinstance(result, UnitKitchenPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return KitchenPartialStatisticsReport(results=kitchen_partial_statistics, errors=errors)


@router.post(
    path='/v1/reports/bonus-system',
    response_model=list[UnitBonusSystemStatistics],
)
@cache(expire=60, namespace='bonus-system')
async def get_bonus_system_statistics(
        units: UnitIdsAndNamesIn = Body(),
        cookies: dict = Body(),
):
    period = Period.today()
    unit_ids = {unit.id for unit in units}
    unit_name_to_id = {unit.name: unit.id for unit in units}
    all_orders = await get_restaurant_orders(cookies, unit_ids, period)
    existing_unit_ids = set()

    results = []
    for name, orders in all_orders:
        unit_id = unit_name_to_id[name]
        existing_unit_ids.add(unit_id)
        orders_with_phone_numbers_count = len(orders[orders['№ телефона'].notnull()].index)
        total_orders_count = len(orders.index)
        orders_with_phone_numbers_percent = 0
        if total_orders_count != 0:
            orders_with_phone_numbers_percent = round(100 * orders_with_phone_numbers_count / total_orders_count)

        results.append(UnitBonusSystemStatistics(
            unit_id=unit_id,
            orders_with_phone_numbers_count=orders_with_phone_numbers_count,
            orders_with_phone_numbers_percent=orders_with_phone_numbers_percent,
            total_orders_count=total_orders_count,
        ))
    missing_unit_ids = unit_ids - existing_unit_ids
    results += [UnitBonusSystemStatistics(unit_id=unit_id) for unit_id in missing_unit_ids]
    return results


@router.post(
    path='/v1/reports/trips-with-one-order',
    response_model=list[models.TripsWithOneOrder],
)
async def on_get_trips_with_one_order(
        unit_ids: set[int] = Body(),
        cookies: dict = Body(),
):
    with httpx.Client(cookies=cookies) as client:
        delivery_statistics_excel = get_delivery_statistics_excel(client, unit_ids, Period.today())
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp_file:
        temp_file.write(delivery_statistics_excel)
        return DeliveryStatisticsExcelParser(temp_file.name).parse()
