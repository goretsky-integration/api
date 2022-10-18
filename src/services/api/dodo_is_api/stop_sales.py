import asyncio
from enum import Enum
from typing import Iterable, Generic, TypeVar, Type

import httpx

from services import parsers
from utils import time_utils, exceptions

__all__ = (
    'get_street_stop_sales',
    'get_sector_stop_sales',
)

RM = TypeVar('RM')


class StopType(Enum):
    UNIT = 0
    STREET = 3
    SECTOR = 4


class StopSalesByCookies(Generic[RM]):

    def __init__(self, url: str, stop_type: StopType, parser: Type[parsers.HTMLParser]):
        self._stop_type = stop_type.value
        self._url = url
        self._parser = parser

    async def request(self, cookies: dict, unit_ids: Iterable[int], period: time_utils.Period) -> RM:
        body = {
            'UnitsIds': tuple(unit_ids),
            'stop_type': self._stop_type,
            'productOrIngredientStopReasons': tuple(range(7)),
            'beginDate': period.from_datetime,
            'endDate': period.to_datetime,
        }
        async with httpx.AsyncClient(cookies=cookies) as client:
            response = await client.post(self._url, data=body, timeout=30)
            if not response.is_success:
                raise exceptions.DodoISAPIError
            return self._parser(response.text).parse()

    def __call__(self, cookies: dict, unit_ids: Iterable[int], period: time_utils.Period):
        return self.request(cookies, unit_ids, period)


get_street_stop_sales = StopSalesByCookies(
    url='https://officemanager.dodopizza.ru/Reports/StopSaleStatistic/GetDeliveryUnitStopSaleReport',
    stop_type=StopType.STREET,
    parser=parsers.StreetStopSalesHTMLParser,
)

get_sector_stop_sales = StopSalesByCookies(
    url='https://officemanager.dodopizza.ru/Reports/StopSaleStatistic/GetDeliverySectorsStopSaleReport',
    stop_type=StopType.SECTOR,
    parser=parsers.SectorStopSalesHTMLParser,
)
