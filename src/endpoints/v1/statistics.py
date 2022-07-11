from fastapi import APIRouter, Body, Query
from pydantic import PositiveInt

import models
from services import convert_models
from services.statistics import partial_statistics, revenue, orders
from utils import time_utils

router = APIRouter(prefix='/v1/statistics', tags=['Statistics'])


@router.get(
    path='/revenue',
    response_model=models.RevenueStatistics,
)
async def get_revenue_statistics(unit_ids: set[PositiveInt] = Query(...)):
    operational_statistics_batch = await revenue.get_operational_statistics(unit_ids)
    return convert_models.operational_statistics_to_revenue_statistics(operational_statistics_batch)


@router.post(
    path='/production/kitchen',
    response_model=models.KitchenProductionStatistics,
)
async def get_kitchen_production_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    kitchen_statistics_batch = await partial_statistics.get_kitchen_statistics(cookies, unit_ids)
    return convert_models.kitchen_statistics_to_production_statistics(kitchen_statistics_batch)


@router.post(
    path='/kitchen/performance',
    response_model=models.KitchenPerformanceStatistics,
)
async def get_kitchen_performance_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    kitchen_statistics_batch = await partial_statistics.get_kitchen_statistics(cookies, unit_ids)
    return convert_models.kitchen_statistics_to_kitchen_performance(kitchen_statistics_batch)


@router.post(
    path='/delivery/performance',
    response_model=models.DeliveryPerformanceStatistics,
)
async def get_delivery_performance_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    delivery_statistics_batch = await partial_statistics.get_delivery_statistics(cookies, unit_ids)
    return convert_models.delivery_statistics_to_delivery_performance(delivery_statistics_batch)


@router.post(
    path='/delivery/heated-shelf',
    response_model=models.HeatedShelfStatistics,
)
async def get_heated_shelf_time_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    delivery_statistics_batch = await partial_statistics.get_delivery_statistics(cookies, unit_ids)
    return convert_models.delivery_statistics_to_heated_shelf_time(delivery_statistics_batch)


@router.post(
    path='/delivery/couriers',
    response_model=models.CouriersStatistics,
)
async def get_couriers_statistics(cookies: dict = Body(...), unit_ids: set[int] = Body(...)):
    delivery_statistics_batch = await partial_statistics.get_delivery_statistics(cookies, unit_ids)
    return convert_models.delivery_statistics_to_couriers_statistics(delivery_statistics_batch)


@router.post(
    path='/bonus-system',
    response_model=list[models.dodo_is_api.orders.UnitBonusSystem],
)
async def get_bonus_system_statistics(
        cookies: dict,
        units: list[models.UnitIdAndName],
):
    period = time_utils.Period.new_today()
    restaurant_orders = await orders.get_restaurant_orders(cookies, units, period)
    return convert_models.restaurant_orders_to_bonus_system_statistics(restaurant_orders)


@router.post(
    path='/being-late-certificates',
    response_model=list[models.UnitBeingLateCertificatesTodayAndWeekBefore],
)
async def get_being_late_certificates_today_and_week_before(
        cookies: dict = Body(...),
        unit_ids_and_names: list[models.UnitIdAndName] = Body(...),
):
    return await orders.get_being_late_certificates_statistics(cookies, unit_ids_and_names)
