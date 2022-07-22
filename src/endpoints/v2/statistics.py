from uuid import UUID

from fastapi import APIRouter, Query

import models
import models.private_dodo_api
from services import convert_models
from services.api import private_dodo_api
from services.statistics import delivery
from utils import time_utils

router = APIRouter(prefix='/v2/statistics', tags=['Statistics'])


@router.get(
    path='/delivery/speed',
    response_model=list[models.UnitDeliverySpeed],
)
async def get_delivery_speed(
        token: str,
        unit_uuids: list[UUID] = Query(...),
):
    period_today = time_utils.Period.new_today()
    units_delivery_statistics = await delivery.get_delivery_statistics(token, unit_uuids, period_today)
    return convert_models.delivery_statistics_to_delivery_speed(units_delivery_statistics)


@router.get(
    path='/production/handover-time',
    response_model=list[models.UnitOrdersHandoverTime],
)
async def get_orders_handover_time_statistics(
        token: str = Query(...),
        unit_uuids: list[UUID] = Query(...),
        sales_channels: list[models.private_dodo_api.SalesChannel] = Query(...),
):
    period = time_utils.Period.new_today()
    orders_handover_time = await private_dodo_api.get_orders_handover_time(token, unit_uuids, period)
    filtered = convert_models.filter_orders_handover_time_by_sales_channels(orders_handover_time, sales_channels)
    return convert_models.calculate_units_average_orders_handover_time(filtered, sales_channels)
