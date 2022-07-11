import re
import unicodedata
from abc import ABC, abstractmethod
from typing import Any, Iterable

import pandas as pd
from bs4 import BeautifulSoup

import models.dodo_is_api.partial_statistics.delivery as delivery_models
import models.dodo_is_api.partial_statistics.kitchen as kitchen_models

__all__ = (
    'PartialStatisticsParser',
    'KitchenStatisticsParser',
    'BeingLateCertificatesParser',
    'DeliveryStatisticsHTMLParser',
)

import models.dodo_is_api.partial_statistics.kitchen


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


class KitchenStatisticsParser(PartialStatisticsParser):
    __slots__ = ('_soup',)

    def parse_panel_titles(self) -> list[str]:
        return [self.clear_extra_symbols(i.text)
                for i in self._soup.find_all('h1', class_='operationalStatistics_panelTitle')]

    def parse_kitchen_revenue(self) -> kitchen_models.KitchenRevenue:
        per_hour, delta_from_week_before = self._panel_titles[0].split('\n')
        return kitchen_models.KitchenRevenue(per_hour=per_hour, delta_from_week_before=delta_from_week_before)

    def parse_product_spending(self) -> kitchen_models.ProductSpending:
        per_hour, delta_from_week_before = self._panel_titles[1].split('\n')
        return kitchen_models.ProductSpending(per_hour=per_hour, delta_from_week_before=delta_from_week_before)

    def parse_tracking(self) -> kitchen_models.Tracking:
        postponed, in_queue, in_work = [
            int(i.text) for i in
            self._soup.find_all('h1', class_='operationalStatistics_productsCountValue')
        ]
        return kitchen_models.Tracking(postponed=postponed, in_queue=in_queue, in_work=in_work)

    def parse_average_cooking_time(self) -> int:
        minutes, seconds = map(int, self._panel_titles[3].split(':'))
        return minutes * 60 + seconds

    def parse(self) -> kitchen_models.KitchenWorkPartial:
        return kitchen_models.KitchenWorkPartial(
            unit_id=self._unit_id,
            revenue=self.parse_kitchen_revenue(),
            product_spending=self.parse_product_spending(),
            average_cooking_time=self.parse_average_cooking_time(),
            tracking=self.parse_tracking()
        )


class BeingLateCertificatesParser(HTMLParser):

    def __init__(self, html: str, request_unit_id: int, units: Iterable[models.UnitIdAndName]):
        super().__init__(html)
        self._request_unit_id = request_unit_id
        self._unit_id_to_unit: dict[int, models.UnitIdAndName] = {unit.unit_id: unit for unit in units}
        self._unit_name_to_unit: dict[str, models.UnitIdAndName] = {unit.unit_name: unit for unit in units}

    def parse(self) -> list[models.UnitBeingLateCertificates]:
        if 'данные не найдены' in self._soup.text.strip().lower():
            return []
        df = pd.read_html(self._html)[1]
        if len(df.columns) == 7:
            return [
                models.UnitBeingLateCertificates(
                    unit_id=self._request_unit_id,
                    unit_name=self._unit_id_to_unit[self._request_unit_id].unit_name,
                    being_late_certificates_count=len(df.index),
                )
            ]
        return [
            models.UnitBeingLateCertificates(
                unit_id=self._unit_name_to_unit[unit_name].unit_id,
                unit_name=unit_name,
                being_late_certificates_count=len(group.index)
            ) for unit_name, group in df.groupby('Пиццерия')
        ]


class DeliveryStatisticsHTMLParser(PartialStatisticsParser):

    def parse_panel_titles(self) -> list[str]:
        return [self.clear_extra_symbols(i.text)
                for i in self._soup.find_all('h1', class_='operationalStatistics_panelTitle')]

    def parse_delivery_performance(self) -> delivery_models.Performance:
        deliveries_amount_per_hour, deliveries_percent = self._panel_titles[0].split('\n')
        orders_week_before = self._soup.find(class_='operationalStatistics_weekAgo').text.strip()
        orders_week_before = re.findall(r'[0-9],[0-9]', orders_week_before)[0].replace(',', '.')
        return delivery_models.Performance(
            orders_for_courier_count_per_hour_today=deliveries_amount_per_hour,
            delta_from_week_before=deliveries_percent,
            orders_for_courier_count_per_hour_week_before=orders_week_before
        )

    def parse_couriers(self) -> delivery_models.Couriers:
        couriers_total_count, couriers_in_queue_count = self._panel_titles[3].split('/')
        return delivery_models.Couriers(in_queue_count=couriers_in_queue_count, total_count=couriers_total_count)

    def parse_heated_shelf(self) -> delivery_models.HeatedShelf:
        orders_on_heated_shelf_count = self._panel_titles[2]
        minutes, seconds = map(int, self._panel_titles[5].split(':'))
        orders_on_heated_shelf_time = minutes * 60 + seconds
        return delivery_models.HeatedShelf(orders_count=orders_on_heated_shelf_count,
                                           orders_awaiting_time=orders_on_heated_shelf_time)

    def parse(self) -> delivery_models.DeliveryWorkPartial:
        return delivery_models.DeliveryWorkPartial(
            unit_id=self._unit_id,
            performance=self.parse_delivery_performance(),
            heated_shelf=self.parse_heated_shelf(),
            couriers=self.parse_couriers(),
        )
