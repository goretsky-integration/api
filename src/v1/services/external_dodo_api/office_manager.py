from typing import Iterable

import pandas as pd
from pandas.core.groupby import DataFrameGroupBy

from services.http_client_factories import HTTPClient
from v1 import exceptions, models, parsers
from v2.periods import Period

__all__ = ('OfficeManagerAPI',)


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

    async def get_restaurant_orders(
            self,
            unit_ids: Iterable[int | str],
            period: Period,
    ) -> DataFrameGroupBy:
        url = 'https://officemanager.dodopizza.ru/Reports/Orders/Get'
        request_data = {
            'filterType': 'OrdersFromRestaurant',
            'unitsIds': tuple(unit_ids),
            'OrderSources': 'Restaurant',
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
            'orderTypes': ['Delivery', 'Pickup', 'Stationary']
        }
        response = await self.__client.post(url, data=request_data)
        return pd.read_html(response.text)[0].groupby('Отдел')

    async def get_stop_sales_by_sectors(self, period: Period, unit_ids: set[int]) -> list[models.StopSaleBySector]:
        request_data = {
            'UnitsIds': tuple(unit_ids),
            'stop_type': 4,
            'productOrIngredientStopReasons': tuple(range(7)),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
        }
        url = '/Reports/StopSaleStatistic/GetDeliverySectorsStopSaleReport'
        response = await self.__client.post(url, data=request_data)
        return parsers.SectorStopSalesHTMLParser(response.text).parse()

    async def get_stop_sales_by_streets(self, period: Period, unit_ids: set[int]) -> list[models.StopSaleByStreet]:
        request_data = {
            'UnitsIds': tuple(unit_ids),
            'stop_type': 3,
            'productOrIngredientStopReasons': tuple(range(7)),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
        }
        url = '/Reports/StopSaleStatistic/GetDeliveryUnitStopSaleReport'
        response = await self.__client.post(url, data=request_data)
        return parsers.StreetStopSalesHTMLParser(response.text).parse()
