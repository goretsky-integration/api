import pathlib

import models.dodo_is_api.partial_statistics.delivery as delivery_models
from core.config import ROOT_PATH
from services.parsers.html import DeliveryStatisticsHTMLParser

HTML_FILES_PATH = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'test_parsers', 'html')


def test_delivery_work_partial_parser():
    with open(HTML_FILES_PATH / 'delivery_work_partial.html', encoding='utf-8') as file:
        html = file.read()
    expected = delivery_models.DeliveryWorkPartial(
        unit_id=389,
        performance=delivery_models.Performance(
            orders_for_courier_count_per_hour_today=2.1,
            orders_for_courier_count_per_hour_week_before=1.8,
            delta_from_week_before=16,
        ),
        heated_shelf=delivery_models.HeatedShelf(
            orders_count=1,
            orders_awaiting_time=321,
        ),
        couriers=delivery_models.Couriers(
            in_queue_count=4,
            total_count=9,
        ),
    )
    assert DeliveryStatisticsHTMLParser(html, 389).parse() == expected
