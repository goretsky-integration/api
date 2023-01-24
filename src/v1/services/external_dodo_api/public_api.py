import asyncio
from dataclasses import dataclass
from typing import Iterable

from services.http_client_factories import HTTPClient
from v1 import models, exceptions

__all__ = ('DodoPublicAPI', 'get_operational_statistics_for_today_and_week_before_batch')


class DodoPublicAPI:

    def __init__(self, client: HTTPClient):
        self.__client = client

    async def get_operational_statistics_for_today_and_week_before(
            self,
            unit_id: int,
    ) -> models.UnitOperationalStatisticsForTodayAndWeekBefore:
        url = f'/OperationalStatisticsForTodayAndWeekBefore/{unit_id}'
        response = await self.__client.get(url=url)
        if not response.is_success:
            raise exceptions.UnitIDAPIError(unit_id=unit_id)
        return models.UnitOperationalStatisticsForTodayAndWeekBefore.parse_obj(response.json())


@dataclass(frozen=True, slots=True)
class OperationalStatisticsBatchDTO:
    results: list[models.UnitOperationalStatisticsForTodayAndWeekBefore]
    errors: list[int]


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
        *,
        dodo_public_api: DodoPublicAPI,
        unit_ids: Iterable[int | str],
) -> OperationalStatisticsBatchDTO:
    tasks = [dodo_public_api.get_operational_statistics_for_today_and_week_before(unit_id) for unit_id in unit_ids]
    responses = await asyncio.gather(*tasks, return_exceptions=True)
    return group_responses(responses)
