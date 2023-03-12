import asyncio

from fastapi import APIRouter, Depends, Query

from api import common_schemas
from api.v1 import schemas, dependencies
from core import exceptions
from models.external_api_responses import office_manager as office_manager_models
from services.external_dodo_api import OfficeManagerAPI
from services.http_client_factories import AsyncHTTPClient

router = APIRouter(prefix='/v1/{country_code}', tags=['Stocks'])


@router.get(
    path='/stocks',
)
async def get_ingredient_stocks(
        unit_ids: common_schemas.UnitIDs = Query(),
        days_left_threshold: int = Query(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_office_manager_api_client),
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
    return office_manager_models.StockBalanceStatistics(units=stocks_balances, error_unit_ids=errors)
