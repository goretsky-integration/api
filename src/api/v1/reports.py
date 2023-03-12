import asyncio
import tempfile

from fastapi import APIRouter, Query, Body, Depends
from fastapi_cache.decorator import cache

from api import common_schemas
from api.v1 import schemas, dependencies
from core import exceptions
from models.domain import sales as sales_models
from models.external_api_responses import office_manager as office_manager_models
from services import parsers
from services.domain import sales as sales_services
from services.external_dodo_api import DodoPublicAPI, OfficeManagerAPI
from services.external_dodo_api import public_api as public_api_services
from services.http_client_factories import AsyncHTTPClient
from services.periods import Period

router = APIRouter(prefix='/v1/{country_code}/reports', tags=['Reports'])


@router.get(
    path='/revenue',
)
@cache(expire=60, namespace='revenue')
async def get_revenue_statistics(
        closing_public_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_public_api_client),
        unit_ids: common_schemas.UnitIDs = Query(),
) -> schemas.RevenueStatisticsReport:
    async with closing_public_api_client as client:
        api = DodoPublicAPI(client)
        units_statistics = await public_api_services.get_operational_statistics_for_today_and_week_before_batch(
            dodo_public_api=api, unit_ids=unit_ids
        )
    units_revenue = sales_services.calculate_units_revenue(units_statistics.results)
    total_revenue = sales_services.calculate_total_revenue(units_statistics.results)
    return sales_models.RevenueStatisticsReport(
        results=sales_models.UnitsRevenueStatistics(units=units_revenue, total=total_revenue),
        errors=units_statistics.errors,
    )


@router.get(
    path='/awaiting-orders',
)
@cache(expire=60, namespace='awaiting-orders')
async def get_delivery_partial_statistics(
        unit_ids: common_schemas.UnitIDs = Query(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> schemas.DeliveryPartialStatisticsReport:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        tasks = (api.get_delivery_partial_statistics(unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    delivery_partial_statistics = [result for result in results
                                   if isinstance(result, office_manager_models.UnitDeliveryPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return office_manager_models.DeliveryPartialStatisticsReport(results=delivery_partial_statistics, errors=errors)


@router.get(
    path='/kitchen-productivity',
)
@cache(expire=60, namespace='kitchen-productivity')
async def get_kitchen_partial_statistics(
        unit_ids: common_schemas.UnitIDs = Query(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> schemas.KitchenPartialStatisticsReport:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        tasks = (api.get_kitchen_partial_statistics(unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    kitchen_partial_statistics = [result for result in results
                                  if isinstance(result, office_manager_models.UnitKitchenPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return office_manager_models.KitchenPartialStatisticsReport(results=kitchen_partial_statistics, errors=errors)


@router.post(
    path='/bonus-system',
)
async def get_bonus_system_statistics(
        unit_ids_and_names: common_schemas.UnitIDsAndNames = Body(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> list[schemas.UnitBonusSystemStatistics]:
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

        results.append(sales_models.UnitBonusSystemStatistics(
            unit_id=unit_id,
            orders_with_phone_numbers_count=orders_with_phone_numbers_count,
            orders_with_phone_numbers_percent=orders_with_phone_numbers_percent,
            total_orders_count=total_orders_count,
        ))
    missing_unit_ids = unit_ids - existing_unit_ids
    results += [sales_models.UnitBonusSystemStatistics(unit_id=unit_id) for unit_id in missing_unit_ids]
    return results


@router.get(
    path='/trips-with-one-order',
)
async def on_get_trips_with_one_order(
        unit_ids: common_schemas.UnitIDs = Query(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
) -> list[schemas.TripsWithOneOrder]:
    period = Period.today()
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        delivery_statistics_excel = await api.get_delivery_statistics_excel(unit_ids, period)
    with tempfile.NamedTemporaryFile(suffix='.xlsx') as temp_file:
        temp_file.write(delivery_statistics_excel)
        return parsers.DeliveryStatisticsExcelParser(temp_file.name).parse()
