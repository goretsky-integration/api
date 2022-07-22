import pathlib

import pytest
from pydantic import parse_raw_as

import models
from core.config import ROOT_PATH
from services.convert_models.production import (
    filter_orders_handover_time_by_sales_channels
)


@pytest.fixture
def orders_handover_time() -> list[models.OrdersHandoverTime]:
    file_path = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'api_responses', 'orders_handover_time.json')
    with open(file_path) as file:
        return parse_raw_as(list[models.OrdersHandoverTime], file.read())


@pytest.mark.parametrize(
    'allowed_sales_channels,count',
    [
        ([models.SalesChannel.TAKEAWAY], 3),
        ([models.SalesChannel.DELIVERY], 29),
        ([models.SalesChannel.DINE_IN], 31),
        ([models.SalesChannel.TAKEAWAY, models.SalesChannel.DELIVERY], 32),
        ([models.SalesChannel.TAKEAWAY, models.SalesChannel.DINE_IN], 34),
        ([models.SalesChannel.DELIVERY, models.SalesChannel.DINE_IN], 60),
        ([models.SalesChannel.DELIVERY, models.SalesChannel.DINE_IN, models.SalesChannel.TAKEAWAY], 63),
    ]
)
def test_filter_orders_handover_time_by_sales_channels(orders_handover_time, allowed_sales_channels, count):
    filtered = filter_orders_handover_time_by_sales_channels(orders_handover_time, allowed_sales_channels)
    assert len(filtered) == count
    for order_handover_time in filtered:
        assert order_handover_time.sales_channel in allowed_sales_channels
