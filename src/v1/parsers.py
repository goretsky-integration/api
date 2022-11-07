import unicodedata
from abc import ABC, abstractmethod
from typing import Any

from bs4 import BeautifulSoup

from v1.models import (
    StopSaleBySector,
    StopSaleByStreet,
    UnitDeliveryPartialStatistics,
    UnitKitchenPartialStatistics,
    StockBalance,
)

__all__ = (
    'PartialStatisticsParser',
    'HTMLParser',
    'SectorStopSalesHTMLParser',
    'StreetStopSalesHTMLParser',
    'DeliveryStatisticsHTMLParser',
    'KitchenStatisticsHTMLParser',
    'StockBalanceHTMLParser',
)


class HTMLParser(ABC):

    def __init__(self, html: str):
        self._html = html
        self._soup = BeautifulSoup(html, 'lxml')

    @abstractmethod
    def parse(self) -> Any:
        pass

    @staticmethod
    def clear_extra_symbols(text: str) -> str:
        text = unicodedata.normalize('NFKD', text)
        for i in (' ', '₽', '%', '\r', '\t'):
            text = text.replace(i, '')
        return text.strip().replace(',', '.').replace('−', '-')


class PartialStatisticsParser(HTMLParser):

    def __init__(self, html: str, unit_id: int | str):
        super().__init__(html)
        self._unit_id = unit_id
        self._panel_titles = self.parse_panel_titles()

    @abstractmethod
    def parse_panel_titles(self) -> list[str]:
        pass


class SectorStopSalesHTMLParser(HTMLParser):
    def parse(self) -> list[StopSaleBySector]:
        trs = self._soup.find('table', id='bootgrid-table').find('tbody').find_all('tr')
        nested_trs = [[td.text.strip() for td in tr.find_all('td')] for tr in trs]
        return [
            StopSaleBySector(
                unit_name=tds[0],
                sector=tds[1],
                started_at=tds[2],
                staff_name_who_stopped=tds[3],
                staff_name_who_resumed=tds[5],
            ) for tds in nested_trs
        ]


class StreetStopSalesHTMLParser(HTMLParser):
    def parse(self) -> list[StopSaleByStreet]:
        trs = self._soup.find('table', id='bootgrid-table').find_all('tr')[1:]
        nested_trs = [[td.text.strip() for td in tr.find_all('td')] for tr in trs]
        return [
            StopSaleByStreet(
                unit_name=tds[0],
                started_at=tds[3],
                staff_name_who_stopped=tds[4],
                staff_name_who_resumed=tds[6],
                sector=tds[1],
                street=tds[2],
            ) for tds in nested_trs
        ]


class DeliveryStatisticsHTMLParser(PartialStatisticsParser):

    def parse_panel_titles(self) -> list[str]:
        return [self.clear_extra_symbols(i.text)
                for i in self._soup.find_all('h1', class_='operationalStatistics_panelTitle')]

    def parse(self) -> UnitDeliveryPartialStatistics:
        couriers_on_shift_count, couriers_in_queue_count = self._panel_titles[3].split('/')
        return UnitDeliveryPartialStatistics(
            unit_id=self._unit_id,
            heated_shelf_orders_count=self._panel_titles[2],
            couriers_in_queue_count=couriers_in_queue_count,
            couriers_on_shift_count=couriers_on_shift_count,
        )


class KitchenStatisticsHTMLParser(PartialStatisticsParser):
    __slots__ = ('_soup',)

    def parse_panel_titles(self) -> list[str]:
        return [self.clear_extra_symbols(i.text)
                for i in self._soup.find_all('h1', class_='operationalStatistics_panelTitle')]

    def parse(self) -> UnitKitchenPartialStatistics:
        sales_per_labor_hour_today, from_week_before_percent = self._panel_titles[0].split('\n')
        minutes, seconds = map(int, self._panel_titles[3].split(':'))
        total_cooking_time = minutes * 60 + seconds
        return UnitKitchenPartialStatistics(
            unit_id=self._unit_id,
            sales_per_labor_hour_today=sales_per_labor_hour_today,
            from_week_before_percent=from_week_before_percent,
            total_cooking_time=total_cooking_time,
        )


class StockBalanceHTMLParser(HTMLParser):

    def __init__(self, html: str, unit_id: int):
        super().__init__(html)
        self.unit_id = unit_id

    def parse(self) -> list[StockBalance]:
        trs = self._soup.find('tbody').find_all('tr')
        result: list[StockBalance] = []
        for tr in trs:
            tds = tr.find_all('td')
            if len(tds) != 6:
                continue
            ingredient_name, stocks_count, _, _, _, days_left = [td.text.strip() for td in tds]
            if not days_left.isdigit():
                continue
            *ingredient_name_parts, stocks_unit = ingredient_name.split(',')
            ingredient_name = ','.join(ingredient_name_parts)
            result.append(StockBalance(
                unit_id=self.unit_id,
                ingredient_name=ingredient_name,
                days_left=days_left,
                stocks_unit=stocks_unit.strip(),
                stocks_count=stocks_count.strip().replace(',', '.').replace(' ', ''),
            ))
        return result
