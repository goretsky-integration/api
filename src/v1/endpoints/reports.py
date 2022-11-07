from fastapi import APIRouter, Query

from v1.models import RevenueStatisticsReport, CountryCode, UnitsRevenueStatistics, UnitIDsIn
from v1.services import public_dodo_api
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
