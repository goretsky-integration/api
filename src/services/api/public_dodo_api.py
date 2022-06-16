import httpx
from fastapi import HTTPException, status

import models
from core import config


async def get_operational_statistics_for_today_and_week_before(
        unit_id: int | str,
) -> models.OperationalStatisticsForTodayAndWeekBefore:
    url = f'https://publicapi.dodois.io/ru/api/v1/OperationalStatisticsForTodayAndWeekBefore/{unit_id}'
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient() as client:
        response = await client.get(url=url, headers=headers)
        if not response.is_success:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
        return models.OperationalStatisticsForTodayAndWeekBefore.parse_obj(response.json())
