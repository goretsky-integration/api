import asyncio
from dataclasses import dataclass
from typing import Iterable

import httpx

from core import config
from v1 import exceptions, models

__all__ = (
    'get_operational_statistics_for_today_and_week_before',
    'get_operational_statistics_for_today_and_week_before_batch',
)


@dataclass(frozen=True, slots=True)
class OperationalStatisticsBatchDTO:
    results: list[models.UnitOperationalStatisticsForTodayAndWeekBefore]
    errors: list[int]


async def get_operational_statistics_for_today_and_week_before(
        client: httpx.AsyncClient,
        country_code: str,
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
    url = f'https://publicapi.dodois.io/{country_code}/api/v1/OperationalStatisticsForTodayAndWeekBefore/{unit_id}'
    headers = {'User-Agent': config.APP_USER_AGENT}
    response = await client.get(url=url, headers=headers)
    if not response.is_success:
        raise exceptions.UnitIDAPIError(unit_id=unit_id)
    return models.UnitOperationalStatisticsForTodayAndWeekBefore.parse_obj(response.json())


def group_responses(responses) -> OperationalStatisticsBatchDTO:
    results: list[models.UnitOperationalStatisticsForTodayAndWeekBefore] = []
    error_unit_ids: list[int] = []

    for response in responses:
        match response:
            case models.UnitOperationalStatisticsForTodayAndWeekBefore():
                results.append(response)
            case exceptions.UnitIDAPIError():
                error_unit_ids.append(response.unit_id)
    return OperationalStatisticsBatchDTO(results=results, errors=error_unit_ids)


async def get_operational_statistics_for_today_and_week_before_batch(
        country_code: str,
        unit_ids: Iterable[int | str],
) -> OperationalStatisticsBatchDTO:
    """Get operational statistics for batch of units more quickly.

    Args:
        unit_ids: collection of unit ids.

    Returns:
        Object that contains ``models.OperationalStatisticsForTodayAndWeekBefore``
        and unit ids of unsuccessful responses.
    """
    async with httpx.AsyncClient(timeout=60) as client:
        tasks = (
            get_operational_statistics_for_today_and_week_before(client, country_code, unit_id)
            for unit_id in unit_ids
        )
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    return group_responses(responses)
