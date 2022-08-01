import pathlib

import pytest

from core.config import ROOT_PATH
from services.parsers.html import StockBalanceHTMLParser


@pytest.fixture
def stocks_balance() -> str:
    file_path = pathlib.Path.joinpath(ROOT_PATH, 'tests', 'test_parsers', 'html', 'stocks_balance.html')
    with open(file_path, encoding='utf-8') as file:
        return file.read()


def test_stocks_balance_days_left(stocks_balance):
    stocks_balance = StockBalanceHTMLParser(stocks_balance, 465).parse()
    assert len(stocks_balance) == 108
    assert len([stock_balance for stock_balance in stocks_balance if stock_balance.days_left <= 1]) == 108
