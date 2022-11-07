import unicodedata
from abc import ABC, abstractmethod
from typing import Any

from bs4 import BeautifulSoup

from v1.models import StopSaleBySector, StopSaleByStreet

__all__ = (
    'PartialStatisticsParser',
    'HTMLParser',
    'SectorStopSalesHTMLParser',
    'StreetStopSalesHTMLParser',
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
