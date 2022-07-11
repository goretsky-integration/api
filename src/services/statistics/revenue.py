from typing import Iterable

import models
from db.cache import set_in_cache, get_from_cache
from services.api import public_dodo_api
from utils import exceptions


async def get_operational_statistics(unit_ids: Iterable[int]) -> models.OperationalStatisticsBatch:
    unit_ids = set(unit_ids)

    units_operational_statistics: list[models.UnitOperationalStatisticsForTodayAndWeekBefore] = []
    unit_ids_to_get_from_api: list[int] = []
    error_unit_ids: list[int] = []

    for unit_id in unit_ids:
        key = f'operational_statistics@{unit_id}'
        try:
            operational_statistics: models.UnitOperationalStatisticsForTodayAndWeekBefore = await get_from_cache(key)
        except exceptions.DoesNotExistInCache:
            unit_ids_to_get_from_api.append(unit_id)
        else:
            units_operational_statistics.append(operational_statistics)

    if unit_ids_to_get_from_api:
        response = await public_dodo_api.get_operational_statistics_for_today_and_week_before_batch(unit_ids)

        for unit_operational_statistics in response.units:
            key = f'operational_statistics@{unit_operational_statistics.unit_id}'
            await set_in_cache(key, unit_operational_statistics)

        units_operational_statistics += response.units
        error_unit_ids += response.error_unit_ids

    return models.OperationalStatisticsBatch(units=units_operational_statistics, error_unit_ids=error_unit_ids)
