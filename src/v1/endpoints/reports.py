import asyncio

from fastapi import APIRouter, Query, Body

from v1.models import RevenueStatisticsReport, CountryCode, UnitsRevenueStatistics, UnitIDsIn, \
    UnitBeingLateCertificatesTodayAndWeekBefore, UnitIdsAndNamesIn
from v1.services import public_dodo_api
from v1.services.being_late_certificates import get_being_late_certificates, zip_certificates_today_and_week_before
from v1.services.operational_statistics import calculate_units_revenue, calculate_total_revenue
from v2.periods import Period

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
    path='/v1/reports/being-late-certificates',
    response_model=list[UnitBeingLateCertificatesTodayAndWeekBefore],
)
async def get_being_late_certificates_today_and_week_before_statistics(
        unit_ids_and_names: UnitIdsAndNamesIn,
        cookies: dict = Body(...)
):
    today = Period.today()
    week_before = Period.week_ago()
    today_being_late_certificates, week_before_being_late_certificates = await asyncio.gather(
        get_being_late_certificates(cookies, unit_ids_and_names, today),
        get_being_late_certificates(cookies, unit_ids_and_names, week_before),
    )
    return zip_certificates_today_and_week_before(
        unit_ids_and_names, today_being_late_certificates, week_before_being_late_certificates)
