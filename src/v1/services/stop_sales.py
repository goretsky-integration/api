import httpx

from core import config
from v2.periods import Period
from v1 import models, parsers

__all__ = (
    'StopSalesAPI',
)


class StopSalesAPI:

    def __init__(self, cookies: dict):
        self._cookies = cookies

    async def get_stop_sales_by_sectors(self, period: Period, unit_ids: set[int]) -> list[models.StopSaleBySector]:
        body = {
            'UnitsIds': tuple(unit_ids),
            'stop_type': 4,
            'productOrIngredientStopReasons': tuple(range(7)),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
        }
        url = 'https://officemanager.dodopizza.ru/Reports/StopSaleStatistic/GetDeliverySectorsStopSaleReport'
        async with httpx.AsyncClient(cookies=self._cookies) as client:
            response = await client.post(url, data=body, headers={'User-Agent': config.APP_USER_AGENT})
        return parsers.SectorStopSalesHTMLParser(response.text).parse()

    async def get_stop_sales_by_streets(self, period: Period, unit_ids: set[int]) -> list[models.StopSaleByStreet]:
        body = {
            'UnitsIds': tuple(unit_ids),
            'stop_type': 3,
            'productOrIngredientStopReasons': tuple(range(7)),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
        }
        url = 'https://officemanager.dodopizza.ru/Reports/StopSaleStatistic/GetDeliveryUnitStopSaleReport'
        async with httpx.AsyncClient(cookies=self._cookies) as client:
            response = await client.post(url, data=body, headers={'User-Agent': config.APP_USER_AGENT})
        return parsers.StreetStopSalesHTMLParser(response.text).parse()
