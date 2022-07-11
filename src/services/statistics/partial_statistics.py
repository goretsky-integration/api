from typing import Iterable, TypeVar, Type, Callable

import models
from db.cache import set_in_cache, get_from_cache
from services import api
from utils import exceptions

UM = TypeVar('UM', bound=models.KitchenWorkPartial | models.DeliveryWorkPartial)
RM = TypeVar('RM', bound=models.UnitsKitchenPartialStatistics | models.UnitsDeliveryPartialStatistics)


async def get_kitchen_statistics(cookies: dict, unit_ids: Iterable[int]) -> models.UnitsKitchenPartialStatistics:
    return await get_partial_statistics(
        cookies=cookies,
        unit_ids=unit_ids,
        key_name='kitchen_statistics',
        response_model=models.UnitsKitchenPartialStatistics,
        api_method=api.dodo_is_api.get_kitchen_statistics_batch,
    )


async def get_delivery_statistics(cookies: dict, unit_ids: Iterable[int]) -> models.UnitsDeliveryPartialStatistics:
    return await get_partial_statistics(
        cookies=cookies,
        unit_ids=unit_ids,
        key_name='delivery_statistics',
        response_model=models.UnitsDeliveryPartialStatistics,
        api_method=api.dodo_is_api.get_delivery_statistics_batch,
    )


async def get_partial_statistics(
        cookies: dict,
        unit_ids: Iterable[int],
        key_name: str,
        response_model: Type[RM],
        api_method: Callable,
):
    unit_ids = set(unit_ids)

    units_statistics: list[UM] = []
    unit_ids_to_get_from_api: list[int] = []
    error_unit_ids: list[int] = []

    for unit_id in unit_ids:
        key = f'{key_name}@{unit_id}'
        try:
            unit_statistics: UM = await get_from_cache(key)
        except exceptions.DoesNotExistInCache:
            unit_ids_to_get_from_api.append(unit_id)
        else:
            units_statistics.append(unit_statistics)

    if unit_ids_to_get_from_api:
        response = await api_method(cookies, unit_ids_to_get_from_api)

        for unit_statistics in response.units:
            key = f'{key_name}@{unit_statistics.unit_id}'
            await set_in_cache(key, unit_statistics)

        units_statistics += response.units
        error_unit_ids += response.error_unit_ids

    return response_model(units=units_statistics, error_unit_ids=error_unit_ids)
