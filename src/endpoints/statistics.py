import uuid
from datetime import datetime, date

from fastapi import APIRouter, Query, Body
from pydantic import PositiveInt

import models
from services import statistics
from services.api import dodo_is_api, private_dodo_api, public_dodo_api
from services.parsers.orders import parse_restaurant_orders_dataframe
from utils import time_utils
from utils.calculations import (
    calculate_revenue_metadata,
)
from utils.convert_models import (
    weekly_operational_statistics_to_revenue_statistics,
    extend_unit_delivery_statistics,
)

router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get(
    path='/revenue',
    response_model=models.UnitsRevenueStatistics,
)
async def get_revenue_statistics(unit_ids: set[PositiveInt] = Query(...)):
    responses = await public_dodo_api.get_operational_statistics_for_today_and_week_before_batch(unit_ids)
    revenue_statistics = [weekly_operational_statistics_to_revenue_statistics(response)
                          for response in responses.success_responses]
    revenue_metadata = calculate_revenue_metadata(revenue_statistics)
    return models.UnitsRevenueStatistics(
        revenues=revenue_statistics,
        metadata=revenue_metadata,
        error_unit_ids=responses.error_unit_ids,
    )


@router.post(
    path='/restaurant-orders',
    response_model=list[models.RestaurantOrdersStatistics]
)
async def get_restaurant_orders_statistics(cookies: dict = Body(...), unit_ids: list[int] = Body(...)):
    current_date = time_utils.get_moscow_datetime_now().strftime('%d.%m.%Y')
    orders = await dodo_is_api.get_restaurant_orders(cookies, unit_ids, current_date)
    return parse_restaurant_orders_dataframe(orders)


@router.post(
    path='/kitchen',
    response_model=models.KitchenStatisticsBatch,
)
async def get_kitchen_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    return await dodo_is_api.get_kitchen_statistics_batch(cookies, unit_ids)


@router.get(
    path='/delivery',
    response_model=list[models.UnitDeliveryStatisticsExtended],
    response_model_by_alias=False,
)
async def get_delivery_statistics(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
        from_datetime: datetime | None = Query(None, description='If datetime is not specified, today will be set'),
        to_datetime: datetime | None = Query(None, description='If datetime is not specified, today will be set'),
):
    units_delivery_statistics = await private_dodo_api.get_delivery_statistics(
        token, unit_uuids,
        from_datetime, to_datetime
    )
    return [extend_unit_delivery_statistics(delivery_statistics)
            for delivery_statistics in units_delivery_statistics]


@router.get(
    path='/production',
    response_model=list[models.OrdersHandoverTime],
    response_model_by_alias=False,
)
async def get_production_statistics(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
        from_datetime: datetime | None = Query(None, description='If datetime is not specified, today will be set'),
        to_datetime: datetime | None = Query(None, description='If datetime is not specified, today will be set'),
):
    return await private_dodo_api.get_production_statistics(token, unit_uuids, from_datetime, to_datetime)


@router.post(
    path='/being-late-certificates',
    response_model=list[models.UnitBeingLateCertificates] | models.SingleUnitBeingLateCertificates,
)
async def get_being_late_certificates_statistics(
        cookies: dict = Body(...),
        unit_ids: set[int] = Body(...),
        from_date: date | None = Body(None, description='If date is not specified, today will be set'),
        to_date: date | None = Body(None, description='If date is not specified, today will be set'),
):
    return await dodo_is_api.get_being_late_certificates(cookies, unit_ids, from_date, to_date)


@router.post(
    path='/being-late-certificates/today-and-week-before',
    response_model=list[models.UnitBeingLateCertificatesTodayAndWeekBefore] \
                   | models.SingleUnitBeingLateCertificatesTodayAndWeekBefore
)
async def get_being_late_certificates_today_and_week_before(
        cookies: dict = Body(...),
        unit_ids: set[int] = Body(...),
):
    return await statistics.get_being_late_certificates_statistics(cookies, unit_ids)
