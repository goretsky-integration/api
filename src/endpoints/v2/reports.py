import asyncio
import collections
import uuid

from fastapi import APIRouter, Depends, Query

import models
from endpoints.bearer import AccessTokenBearer
from services.api.private_dodo_api import get_productivity_statistics, get_delivery_statistics, get_channels_stop_sales
from utils import time_utils

__all__ = (
    'router',
)

router = APIRouter(prefix='/v2/statistics', tags=['Reports'])


@router.get(
    path='/productivity-balance/',
    response_model_by_alias=False,
    response_model=list[models.UnitProductivityBalanceStatistics]
)
async def get_productivity_balance(
        token: str = Depends(AccessTokenBearer()),
        unit_uuids: set[uuid.UUID] = Query(),
):
    period = time_utils.Period.new_today()

    productivity_statistics, delivery_statistics, stop_sales_by_sales_channels = await asyncio.gather(
        get_productivity_statistics(token, unit_uuids, period),
        get_delivery_statistics(token, unit_uuids, period),
        get_channels_stop_sales(token, unit_uuids, period),
    )

    unit_uuid_to_productivity_statistics: dict[uuid.UUID, models.UnitProductivityStatistics] = {unit.unit_uuid: unit for unit in productivity_statistics}
    unit_uuid_to_delivery_statistics: dict[uuid.UUID, models.UnitDeliveryStatistics] = {unit.unit_id: unit for unit in delivery_statistics}
    unit_uuid_to_unit_stop_sales: dict[uuid.UUID, list[models.StopSalesBySalesChannels]] = collections.defaultdict(list)
    for stop_sale in stop_sales_by_sales_channels:
        unit_uuid_to_unit_stop_sales[stop_sale.unit_id].append(stop_sale)

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
                ended_at = stop_sale.ended_at
                if stop_sale.ended_at is None:
                    ended_at = period.to_datetime
                stop_duration = ended_at - stop_sale.started_at
                stop_sale_duration_in_seconds += stop_duration.total_seconds()
        response.append(models.UnitProductivityBalanceStatistics(
            unit_uuid=unit_uuid,
            sales_per_labor_hour=sales_per_labor_hour,
            orders_per_labor_hour=orders_per_labor_hour,
            stop_sale_duration_in_seconds=stop_sale_duration_in_seconds,
        ))
    return response
