import asyncio
from typing import Type, Any, Iterable, Callable, TypeVar

import httpx

import models
from core import config
from services import parsers
from utils import exceptions

__all__ = (
    'get_kitchen_statistics',
    'get_delivery_statistics',
    'get_kitchen_statistics_batch',
    'get_delivery_statistics_batch',
)

UM = TypeVar('UM', bound=models.DeliveryWorkPartial | models.KitchenWorkPartial)
RM = TypeVar('RM', bound=models.UnitsKitchenPartialStatistics | models.UnitsDeliveryPartialStatistics)


async def get_kitchen_statistics(
        cookies: dict,
        unit_id: int | str,
) -> models.KitchenWorkPartial:
    url = 'https://officemanager.dodopizza.ru/OfficeManager/OperationalStatistics/KitchenPartial'
    return await request_partial_statistics(cookies, unit_id, url, parsers.KitchenStatisticsParser)


async def get_delivery_statistics(
        cookies: dict,
        unit_id: int | str,
) -> models.DeliveryWorkPartial:
    url = 'https://officemanager.dodopizza.ru/OfficeManager/OperationalStatistics/DeliveryWorkPartial'
    return await request_partial_statistics(cookies, unit_id, url, parsers.DeliveryStatisticsHTMLParser)


async def request_partial_statistics(
        cookies: dict,
        unit_id: int | str,
        url: str,
        parser: Type[parsers.PartialStatisticsParser],
) -> Any:
    params = {'unitId': unit_id}
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.get(url, params=params, timeout=30, headers=headers)
        if not response.is_success:
            raise exceptions.PartialStatisticsAPIError(unit_id=unit_id)
        return parser(response.text, unit_id).parse()


async def request_partial_statistics_batch(
        cookies: dict,
        unit_ids: Iterable[int | str],
        method: Callable,
        unit_model: Type[UM],
        response_model: Type[RM],
):
    tasks = (method(cookies, unit_id) for unit_id in unit_ids)
    responses = await asyncio.gather(*tasks, return_exceptions=True)

    response_statistics: list[UM] = []
    error_unit_ids: list[int] = []

    for response in responses:
        match response:
            case unit_model():
                response_statistics.append(response)
            case exceptions.PartialStatisticsAPIError():
                error_unit_ids.append(response.unit_id)

    return response_model(units=response_statistics, error_unit_ids=error_unit_ids)


async def get_kitchen_statistics_batch(
        cookies: dict,
        unit_ids: Iterable[int | str],
) -> models.UnitsKitchenPartialStatistics:
    return await request_partial_statistics_batch(
        cookies=cookies,
        unit_ids=unit_ids,
        method=get_kitchen_statistics,
        unit_model=models.KitchenWorkPartial,
        response_model=models.UnitsKitchenPartialStatistics,
    )


async def get_delivery_statistics_batch(
        cookies: dict,
        unit_ids: Iterable[int | str],
) -> models.UnitsDeliveryPartialStatistics:
    return await request_partial_statistics_batch(
        cookies=cookies,
        unit_ids=unit_ids,
        method=get_delivery_statistics,
        unit_model=models.DeliveryWorkPartial,
        response_model=models.UnitsDeliveryPartialStatistics,
    )
