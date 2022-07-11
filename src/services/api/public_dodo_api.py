import asyncio
from typing import Iterable, TypeAlias

import httpx

import models
from core import config
from utils import exceptions

__all__ = (
    'get_operational_statistics_for_today_and_week_before',
    'get_operational_statistics_for_today_and_week_before_batch',
)

OperationalStatisticsAPIResponse: TypeAlias = (
        models.UnitOperationalStatisticsForTodayAndWeekBefore | exceptions.OperationalStatisticsAPIError)


async def get_operational_statistics_for_today_and_week_before(
        unit_id: int | str,
) -> models.UnitOperationalStatisticsForTodayAndWeekBefore:
    """Get operational statistics for exact unit.

    Args:
        unit_id: id of unit.

    Returns:
        ``models.OperationalStatisticsForTodayAndWeekBefore`` on success.

    Raises:
        exceptions.OperationalStatisticsAPIError on error with unit id.
    """
    url = f'https://publicapi.dodois.io/ru/api/v1/OperationalStatisticsForTodayAndWeekBefore/{unit_id}'
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers)
        if not response.is_success:
            raise exceptions.OperationalStatisticsAPIError(unit_id=unit_id)
        return models.UnitOperationalStatisticsForTodayAndWeekBefore.parse_obj(response.json())


async def get_operational_statistics_for_today_and_week_before_batch(
        unit_ids: Iterable[int | str],
) -> models.OperationalStatisticsBatch:
    """Get operational statistics for batch of units more quickly.

    Args:
        unit_ids: collection of unit ids.

    Returns:
        Object that contains ``models.OperationalStatisticsForTodayAndWeekBefore``
        and unit ids of unsuccessful responses.
    """
    tasks = (get_operational_statistics_for_today_and_week_before(unit_id) for unit_id in unit_ids)
    responses: tuple[OperationalStatisticsAPIResponse, ...] = await asyncio.gather(*tasks, return_exceptions=True)

    units: list[models.UnitOperationalStatisticsForTodayAndWeekBefore] = []
    error_unit_ids: list[int] = []
    for response in responses:
        match response:
            case models.UnitOperationalStatisticsForTodayAndWeekBefore():
                units.append(response)
            case exceptions.OperationalStatisticsAPIError():
                error_unit_ids.append(response.unit_id)

    return models.OperationalStatisticsBatch(units=units, error_unit_ids=error_unit_ids)
