import asyncio
import collections
import datetime
import statistics
import uuid
from typing import Iterable

from fastapi import APIRouter, Depends, Query

from v2 import models
from v2.endpoints.bearer import AccessTokenBearer
from v2.models import UnitUUIDsIn, CountryCode, UnitProductivityBalanceStatistics, \
    UnitBeingLateCertificatesTodayAndWeekBefore, UnitDeliveryProductivityStatistics
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
            'unit_uuid': unit_uuid,
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
    period = Period.today()
    api = PrivateDodoAPI(token, country_code)
    productivity_statistics, units_delivery_statistics, stop_sales = await asyncio.gather(
        api.get_production_productivity_statistics(period, unit_uuids),
        api.get_delivery_statistics(period, unit_uuids),
        api.get_stop_sales_by_sales_channels(period, unit_uuids),
    )
    unit_uuid_to_productivity_statistics = {unit.unit_uuid: unit for unit in productivity_statistics}
    unit_uuid_to_delivery_statistics = {unit.unit_uuid: unit for unit in units_delivery_statistics}
    unit_uuid_to_unit_stop_sales = collections.defaultdict(list)
    for stop_sale in stop_sales:
        unit_uuid_to_unit_stop_sales[stop_sale.unit_uuid].append(stop_sale)

    response = []
    for unit_uuid in unit_uuids:
        sales_per_labor_hour = 0
        orders_per_labor_hour = 0
        stop_sale_duration_in_seconds = 0
        if unit_uuid in unit_uuid_to_productivity_statistics:
            sales_per_labor_hour = unit_uuid_to_productivity_statistics[unit_uuid].sales_per_labor_hour
        if unit_uuid in unit_uuid_to_delivery_statistics:
            orders_per_labor_hour = unit_uuid_to_delivery_statistics[unit_uuid].orders_per_labor_hour
        if unit_uuid in unit_uuid_to_unit_stop_sales:
            stop_sales = unit_uuid_to_unit_stop_sales[unit_uuid]
            for stop_sale in stop_sales:
                if stop_sale.sales_channel_name != 'Delivery':
                    continue
                ended_at = stop_sale.ended_at
                if stop_sale.ended_at is None:
                    ended_at = period.end
                stop_duration = ended_at - stop_sale.started_at
                stop_sale_duration_in_seconds += stop_duration.total_seconds()
        response.append(models.UnitProductivityBalanceStatistics(
            unit_uuid=unit_uuid,
            sales_per_labor_hour=sales_per_labor_hour,
            orders_per_labor_hour=orders_per_labor_hour,
            stop_sale_duration_in_seconds=stop_sale_duration_in_seconds,
        ))
    return response


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
    response_model=list[UnitDeliveryProductivityStatistics],
)
async def get_delivery_productivity_statistics(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    today_period = Period.today()
    week_before_period = Period.week_before_to_this_time()
    api = PrivateDodoAPI(token, country_code)
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
            response.append(delivery_statistics.to_today_and_week_before_delivery_productivity(
                unit_uuid,
                unit_today_delivery_statistics,
                unit_week_delivery_statistics,
            ))
    return response


@router.get(
    path='/being-late-certificates',
    response_model=list[UnitBeingLateCertificatesTodayAndWeekBefore],
)
async def get_being_late_certificates_for_today_and_week_before(
        country_code: CountryCode,
        unit_uuids: UnitUUIDsIn = Query(),
        token: str = Depends(AccessTokenBearer()),
):
    today_period = Period.today()
    week_before_period = Period.week_before()
    api = PrivateDodoAPI(token, country_code)
    today_units_delivery_statistics, week_before_units_delivery_statistics = await asyncio.gather(
        api.get_delivery_statistics(today_period, unit_uuids),
        api.get_delivery_statistics(week_before_period, unit_uuids),
    )
    unit_uuid_to_today_count = {unit.unit_uuid: unit.late_orders_count for unit in today_units_delivery_statistics}
    unit_uuid_to_week_before_count = {unit.unit_uuid: unit.late_orders_count for unit in
                                      week_before_units_delivery_statistics}
    return [
        UnitBeingLateCertificatesTodayAndWeekBefore(
            unit_uuid=unit_uuid,
            certificates_count_today=unit_uuid_to_today_count.get(unit_uuid, 0),
            certificates_count_week_before=unit_uuid_to_week_before_count.get(unit_uuid, 0),
        ) for unit_uuid in unit_uuids
    ]
