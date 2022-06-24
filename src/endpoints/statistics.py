import uuid

from fastapi import APIRouter, Query
from pydantic import PositiveInt

import models
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
async def get_restaurant_orders_statistics(cookies: dict, unit_ids: list[int]):
    current_date = time_utils.get_moscow_datetime_now().strftime('%d.%m.%Y')
    orders = await dodo_is_api.get_restaurant_orders(cookies, unit_ids, current_date)
    return parse_restaurant_orders_dataframe(orders)


@router.post(
    path='/kitchen',
    response_model=models.KitchenStatistics,
)
async def get_kitchen_statistics(cookies_and_unit_id: models.CookiesAndUnitId):
    return await dodo_is_api.get_kitchen_statistics(
        cookies_and_unit_id.cookies, cookies_and_unit_id.unit_id)


@router.get(
    path='/delivery',
    response_model=list[models.UnitDeliveryStatisticsExtended],
    response_model_by_alias=False,
)
async def get_delivery_statistics(token: str, unit_uuids: list[uuid.UUID] = Query(...)):
    units_delivery_statistics = await private_dodo_api.get_delivery_statistics(token, unit_uuids)
    return [extend_unit_delivery_statistics(delivery_statistics)
            for delivery_statistics in units_delivery_statistics]
