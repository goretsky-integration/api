import unicodedata
from abc import ABC, abstractmethod
from typing import Any, Iterable, Hashable

import pandas as pd
from bs4 import BeautifulSoup

from v1 import models
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


class BeingLateCertificatesParser(HTMLParser):

    def __init__(self, html: str, request_unit_id: int, units: Iterable[models.UnitIdAndNameIn]):
        super().__init__(html)
        self._request_unit_id = request_unit_id
        self._unit_id_to_unit: dict[int, models.UnitIdAndNameIn] = {unit.id: unit for unit in units}
        self._unit_name_to_unit: dict[str | Hashable, models.UnitIdAndNameIn] = {unit.name: unit for unit in units}

    def parse(self) -> list[models.UnitBeingLateCertificates]:
        if 'данные не найдены' in self._soup.text.strip().lower():
            return []
        df = pd.read_html(self._html)[1]
        if len(df.columns) == 7:
            return [
                models.UnitBeingLateCertificates(
                    unit_id=self._request_unit_id,
                    unit_name=self._unit_id_to_unit[self._request_unit_id].name,
                    certificates_count=len(df.index),
                )
            ]
        return [
            models.UnitBeingLateCertificates(
                unit_id=self._unit_name_to_unit[unit_name].id,
                unit_name=unit_name,
                certificates_count=len(group.index)
            ) for unit_name, group in df.groupby('Пиццерия')
        ]
