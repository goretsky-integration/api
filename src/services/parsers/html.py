import unicodedata
from abc import ABC, abstractmethod
from typing import Any

from bs4 import BeautifulSoup

import models

__all__ = (
    'KitchenStatisticsParser',
)


class HTMLParser(ABC):

    def __init__(self, html: str):
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


class KitchenStatisticsParser(HTMLParser):
    __slots__ = ('_soup',)

    def __init__(self, html: str, unit_id: int | str):
        super().__init__(html)
        self._unit_id = unit_id
        self._panel_titles = self.parse_panel_titles()

    def parse_panel_titles(self) -> list[str]:
        return [self.clear_extra_symbols(i.text)
                for i in self._soup.find_all('h1', class_='operationalStatistics_panelTitle')]

    def parse_kitchen_revenue(self) -> models.KitchenRevenue:
        per_hour, delta_from_week_before = self._panel_titles[0].split('\n')
        return models.KitchenRevenue(per_hour=per_hour,
                                     delta_from_week_before=delta_from_week_before)

    def parse_product_spending(self) -> models.ProductSpending:
        per_hour, delta_from_week_before = self._panel_titles[1].split('\n')
        return models.ProductSpending(per_hour=per_hour,
                                      delta_from_week_before=delta_from_week_before)

    def parse_tracking(self) -> models.Tracking:
        postponed, in_queue, in_work = [
            int(i.text) for i in
            self._soup.find_all('h1', class_='operationalStatistics_productsCountValue')
        ]
        return models.Tracking(postponed=postponed, in_queue=in_queue, in_work=in_work)

    def parse_average_cooking_time(self) -> int:
        minutes, seconds = map(int, self._panel_titles[3].split(':'))
        return minutes * 60 + seconds

    def parse(self) -> models.KitchenStatistics:
        return models.KitchenStatistics(
            unit_id=self._unit_id,
            revenue=self.parse_kitchen_revenue(),
            product_spending=self.parse_product_spending(),
            average_cooking_time=self.parse_average_cooking_time(),
            tracking=self.parse_tracking()
        )
