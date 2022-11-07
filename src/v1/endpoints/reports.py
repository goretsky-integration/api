import asyncio

import httpx
from fastapi import APIRouter, Query, Body

from v1 import exceptions
from v1.models import RevenueStatisticsReport, CountryCode, UnitsRevenueStatistics, UnitIDsIn, \
    DeliveryPartialStatisticsReport, UnitDeliveryPartialStatistics, KitchenPartialStatisticsReport, \
    UnitKitchenPartialStatistics
from v1.services import public_dodo_api, operational_statistics
from v1.services.operational_statistics import calculate_units_revenue, calculate_total_revenue

router = APIRouter(tags=['Reports'])


@router.get(
    path='/v1/{country_code}/reports/revenue',
    response_model=RevenueStatisticsReport,
)
async def get_revenue_statistics(
        country_code: CountryCode,
        unit_ids: UnitIDsIn = Query(),
):
    response = await public_dodo_api.get_operational_statistics_for_today_and_week_before_batch(country_code, unit_ids)
    units = calculate_units_revenue(response.results)
    total = calculate_total_revenue(response.results)
    return RevenueStatisticsReport(results=UnitsRevenueStatistics(units=units, total=total), errors=response.errors)


@router.post(
    path='/v1/reports/awaiting-orders',
    response_model=DeliveryPartialStatisticsReport,
)
async def get_delivery_partial_statistics(unit_ids: UnitIDsIn, cookies: dict = Body()):
    async with httpx.AsyncClient(cookies=cookies) as client:
        tasks = (operational_statistics.get_delivery_partial_statistics(client, unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    delivery_partial_statistics = [result for result in results if isinstance(result, UnitDeliveryPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return DeliveryPartialStatisticsReport(results=delivery_partial_statistics, errors=errors)


@router.post(
    path='/v1/reports/kitchen-productivity',
    response_model=KitchenPartialStatisticsReport,
)
async def get_kitchen_partial_statistics(unit_ids: UnitIDsIn, cookies: dict = Body()):
    async with httpx.AsyncClient(cookies=cookies) as client:
        tasks = (operational_statistics.get_kitchen_partial_statistics(client, unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    kitchen_partial_statistics = [result for result in results if isinstance(result, UnitKitchenPartialStatistics)]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return KitchenPartialStatisticsReport(results=kitchen_partial_statistics, errors=errors)
