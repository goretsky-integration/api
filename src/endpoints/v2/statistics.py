import uuid

from fastapi import APIRouter, Query

import models
import models.private_dodo_api
from services import convert_models
from services.statistics import delivery
from utils import time_utils

router = APIRouter(prefix='/v2/statistics', tags=['Statistics'])


@router.get(
    path='/delivery/speed',
    response_model=list[models.UnitDeliverySpeed],
)
async def get_delivery_speed(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
):
    period_today = time_utils.Period.new_today()
    units_delivery_statistics = await delivery.get_delivery_statistics(token, unit_uuids, period_today)
    return convert_models.delivery_statistics_to_delivery_speed(units_delivery_statistics)
