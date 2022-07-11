import asyncio
import uuid
from typing import Iterable

import models
from db.cache import set_in_cache, get_from_cache
from services.api import private_dodo_api
from utils import time_utils, exceptions
from services.convert_models import extend_unit_delivery_statistics


async def get_delivery_statistics(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_config: time_utils.Period,
) -> list[models.UnitDeliveryStatisticsExtended]:
    unit_uuids = set(unit_uuids)

    unit_uuids_to_get_from_api = []
    units_delivery_statistics = []

    for unit_uuid in unit_uuids:
        key = f'delivery_statistics@{unit_uuid.hex}@{datetime_config.from_datetime.isoformat()}'
        try:
            unit_delivery_statistics: models.UnitDeliveryStatisticsExtended = await get_from_cache(key)
        except exceptions.DoesNotExistInCache:
            unit_uuids_to_get_from_api.append(unit_uuid)
        else:
            units_delivery_statistics.append(unit_delivery_statistics)

    if unit_uuids_to_get_from_api:
        units_delivery_statistics_from_api = await private_dodo_api.get_delivery_statistics(
            token, unit_uuids_to_get_from_api, datetime_config)
        units_delivery_statistics_from_api = [extend_unit_delivery_statistics(i) for i in
                                              units_delivery_statistics_from_api]

        for unit_delivery_statistics in units_delivery_statistics_from_api:
            key = (f'delivery_statistics@{unit_delivery_statistics.unit_id.hex}'
                   f'@{datetime_config.from_datetime.isoformat()}')
            await set_in_cache(key, unit_delivery_statistics)

        units_delivery_statistics += units_delivery_statistics_from_api

    return units_delivery_statistics


async def get_delivery_statistics_batch(
        token: str,
        unit_uuids: Iterable[uuid.UUID],
        datetime_configs: Iterable[time_utils.Period]
) -> tuple[list[models.UnitDeliveryStatisticsExtended], ...]:
    tasks = (get_delivery_statistics(token, unit_uuids, datetime_config) for datetime_config in datetime_configs)
    return await asyncio.gather(*tasks)
