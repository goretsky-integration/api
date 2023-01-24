from typing import Iterable

from services.http_client_factories import HTTPClient
from v1 import exceptions, models, parsers

__all__ = ('OfficeManagerAPI',)

from v2.periods import Period


class OfficeManagerAPI:

    def __init__(self, client: HTTPClient):
        self.__client = client

    async def get_delivery_partial_statistics(
            self,
            unit_id: int,
    ) -> models.UnitDeliveryPartialStatistics:
        url = '/OfficeManager/OperationalStatistics/DeliveryWorkPartial'
        params = {'unitId': unit_id}
        response = await self.__client.get(url, params=params)
        if response.is_error:
            raise exceptions.UnitIDAPIError(unit_id=unit_id)
        return parsers.DeliveryStatisticsHTMLParser(response.text, unit_id).parse()

    async def get_kitchen_partial_statistics(
            self,
            unit_id: int,
    ) -> models.UnitKitchenPartialStatistics:
        url = '/OfficeManager/OperationalStatistics/KitchenPartial'
        params = {'unitId': unit_id}
        response = await self.__client.get(url, params=params)
        if response.is_error:
            raise exceptions.UnitIDAPIError(unit_id=unit_id)
        return parsers.KitchenStatisticsHTMLParser(response.text, unit_id).parse()

    async def get_stocks_balance(self, unit_id: int | str) -> list[models.StockBalance]:
        url = '/OfficeManager/StockBalance/Get'
        params = {'unitId': unit_id}
        response = await self.__client.get(url, params=params)
        if response.is_error:
            raise exceptions.UnitIDAPIError(unit_id=unit_id)
        return parsers.StockBalanceHTMLParser(response.text, unit_id).parse()

    async def get_delivery_statistics_excel(self, unit_ids: Iterable[int], period: Period) -> bytes:
        url = '/Reports/DeliveryStatistic/Export'
        request_data = {
            'unitsIds': tuple(unit_ids),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
        }
        response = await self.__client.post(url, data=request_data)
        return response.content
