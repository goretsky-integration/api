from fastapi import APIRouter

import models
from services.api.dodo_is_api import get_restaurant_orders
from services.api import dodo_is_api
from services.api.public_dodo_api import get_operational_statistics_for_today_and_week_before
from services.parsers.orders import parse_restaurant_orders_dataframe
from utils import time_utils
from utils.convert_models import weekly_operational_statistics_to_revenue_statistics

router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get(
    path='/revenue/{unit_id}',
    response_model=models.RevenueForTodayAndWeekBeforeStatistics,
)
async def revenue_for_today_and_week_before_statistics(unit_id: int):
    operational_statistics = await get_operational_statistics_for_today_and_week_before(unit_id)
    return weekly_operational_statistics_to_revenue_statistics(operational_statistics)


@router.post(
    path='/',
    response_model=list[models.RestaurantOrdersStatistics]
)
async def get_restaurant_orders_statistics(cookies: dict, unit_ids: list[int]):
    current_date = time_utils.get_moscow_datetime_now().strftime('%d.%m.%Y')
    orders = await get_restaurant_orders(cookies, unit_ids, current_date)
    return parse_restaurant_orders_dataframe(orders)


@router.post(
    path='/kitchen-statistics',
    response_model=models.KitchenStatistics,
)
async def get_kitchen_statistics(cookies_and_unit_id: models.CookiesAndUnitId):
    return await dodo_is_api.get_kitchen_statistics(
        cookies_and_unit_id.cookies, cookies_and_unit_id.unit_id)
