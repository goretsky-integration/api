import asyncio

from fastapi import APIRouter, Depends, Query

from services.external_dodo_api import OfficeManagerAPI
from services.http_client_factories import HTTPClient
from v1 import exceptions
from v1.endpoints import schemas
from v1.endpoints.dependencies import get_closing_office_manager_api_client
from v1.models import StockBalanceStatistics

router = APIRouter(prefix='/stocks', tags=['Stocks'])


@router.get(
    path='/',
)
async def get_ingredient_stocks(
        unit_ids: schemas.UnitIDs = Query(),
        days_left_threshold: int = Query(),
        closing_office_manager_api_client: HTTPClient = Depends(get_closing_office_manager_api_client),
) -> schemas.StockBalanceStatistics:
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        tasks = (api.get_stocks_balance(unit_id) for unit_id in unit_ids)
        units_stocks_balance = await asyncio.gather(*tasks, return_exceptions=True)
    stocks_balances = [
        ingredient_stocks
        for unit_stocks_balance in units_stocks_balance
        if isinstance(unit_stocks_balance, list)
        for ingredient_stocks in unit_stocks_balance
        if ingredient_stocks.days_left <= days_left_threshold
    ]
    errors = [
        unit_stocks_balance.unit_id for unit_stocks_balance in units_stocks_balance
        if isinstance(unit_stocks_balance, exceptions.UnitIDAPIError)
    ]
    return StockBalanceStatistics(units=stocks_balances, error_unit_ids=errors)
