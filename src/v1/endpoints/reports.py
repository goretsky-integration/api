import asyncio
import tempfile
from typing import Iterable

from fastapi import APIRouter, Query, Body, Depends
from fastapi_cache.decorator import cache

from services.external_dodo_api import (
    DodoPublicAPI,
    OfficeManagerAPI,
    get_operational_statistics_for_today_and_week_before_batch,
)
from services.http_client_factories import HTTPClient
from services.periods import Period
from v1 import exceptions
from v1.endpoints import schemas
from v1.endpoints.dependencies import get_closing_public_api_client, get_closing_office_manager_api_client
from v1.models import (
    RevenueStatisticsReport,
    UnitsRevenueStatistics,
    UnitIDsIn,
    DeliveryPartialStatisticsReport,
    UnitDeliveryPartialStatistics,
    KitchenPartialStatisticsReport,
    UnitKitchenPartialStatistics,
    UnitBonusSystemStatistics,
    UnitIdsAndNamesIn,
)
from v1.parsers import DeliveryStatisticsExcelParser
from v1.services.operational_statistics import calculate_units_revenue, calculate_total_revenue

router = APIRouter(prefix='/v1/{country_code}/reports', tags=['Reports'])


@router.get(
    path='/revenue',
)
@cache(expire=60, namespace='revenue')
async def get_revenue_statistics(
        closing_public_api_client: HTTPClient = Depends(get_closing_public_api_client),
        unit_ids: UnitIDsIn = Query(),
) -> schemas.RevenueStatisticsReport:
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


@router.get(
    path='/awaiting-orders',
)
@cache(expire=60, namespace='awaiting-orders')
async def get_delivery_partial_statistics(
        unit_ids: UnitIDsIn = Query(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> schemas.DeliveryPartialStatisticsReport:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        tasks = (api.get_delivery_partial_statistics(unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    delivery_partial_statistics = [result for result in results if isinstance(result, UnitDeliveryPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return DeliveryPartialStatisticsReport(results=delivery_partial_statistics, errors=errors)


@router.get(
    path='/kitchen-productivity',
)
@cache(expire=60, namespace='kitchen-productivity')
async def get_kitchen_partial_statistics(
        unit_ids: UnitIDsIn = Query(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> schemas.KitchenPartialStatisticsReport:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        tasks = (api.get_kitchen_partial_statistics(unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    kitchen_partial_statistics = [result for result in results if isinstance(result, UnitKitchenPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return KitchenPartialStatisticsReport(results=kitchen_partial_statistics, errors=errors)


@router.post(
    path='/bonus-system',
)
async def get_bonus_system_statistics(
        unit_ids_and_names: UnitIdsAndNamesIn = Body(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> Iterable[schemas.UnitBonusSystemStatistics]:
    period = Period.today()
    unit_ids = {unit.id for unit in unit_ids_and_names}
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        all_orders = await api.get_restaurant_orders(unit_ids, period)
    unit_name_to_id = {unit.name: unit.id for unit in unit_ids_and_names}
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


@router.get(
    path='/trips-with-one-order',
)
async def on_get_trips_with_one_order(
        unit_ids: UnitIDsIn = Query(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> Iterable[schemas.TripsWithOneOrder]:
    period = Period.today()
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        delivery_statistics_excel = await api.get_delivery_statistics_excel(unit_ids, period)
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp_file:
        temp_file.write(delivery_statistics_excel)
        return DeliveryStatisticsExcelParser(temp_file.name).parse()
