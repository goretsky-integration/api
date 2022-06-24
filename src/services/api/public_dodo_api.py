import asyncio
from dataclasses import dataclass
from typing import Iterable, TypeAlias

import httpx

import models
from core import config
from utils import exceptions

__all__ = (
    'get_operational_statistics_for_today_and_week_before',
    'get_operational_statistics_for_today_and_week_before_batch',
    'OperationalStatisticsBatch',
)

OperationalStatisticsAPIResponse: TypeAlias = (
        models.OperationalStatisticsForTodayAndWeekBefore | exceptions.OperationalStatisticsAPIError)


@dataclass(slots=True, frozen=True)
class OperationalStatisticsBatch:
    success_responses: list[models.OperationalStatisticsForTodayAndWeekBefore]
    error_unit_ids: list[int]


async def get_operational_statistics_for_today_and_week_before(
        unit_id: int | str,
) -> models.OperationalStatisticsForTodayAndWeekBefore:
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
        return models.OperationalStatisticsForTodayAndWeekBefore.parse_obj(response.json())


async def get_operational_statistics_for_today_and_week_before_batch(
        unit_ids: Iterable[int | str],
) -> OperationalStatisticsBatch:
    """Get operational statistics for batch of units more quickly.

    Args:
        unit_ids: collection of unit ids.

    Returns:
        Object that contains ``models.OperationalStatisticsForTodayAndWeekBefore``
        and unit ids of unsuccessful responses.
    """
    tasks = (get_operational_statistics_for_today_and_week_before(unit_id) for unit_id in unit_ids)
    responses: tuple[OperationalStatisticsAPIResponse, ...] = await asyncio.gather(*tasks, return_exceptions=True)
    return OperationalStatisticsBatch(
        success_responses=[
            response for response in responses
            if isinstance(response, models.OperationalStatisticsForTodayAndWeekBefore)
        ],
        error_unit_ids=[
            response.unit_id for response in responses
            if isinstance(response, exceptions.OperationalStatisticsAPIError)
        ]
    )
