import asyncio

import httpx
from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from core import config
from v1 import exceptions
from v1.models import UnitIDsIn, StockBalance, StockBalanceStatistics
from v1.services.stocks import get_stocks_balance

router = APIRouter(prefix='/stocks', tags=['Stocks'])


@router.post(
    path='/',
    response_model=StockBalanceStatistics,
)
async def get_ingredient_stocks(
        unit_ids: UnitIDsIn,
        cookies: dict = Body(),
        days_left_threshold: int = Body(),
):
    async with httpx.AsyncClient(cookies=cookies, headers={'User-Agent': config.APP_USER_AGENT}) as client:
        tasks = (get_stocks_balance(client, unit_id) for unit_id in unit_ids)
        results = await asyncio.gather(*tasks, return_exceptions=True)
    stocks_balances = [i for result in results if isinstance(result, list)
                       for i in result
                       if i.days_left <= days_left_threshold]
    errors = [result.unit_id for result in results if isinstance(result, exceptions.UnitIDAPIError)]
    return StockBalanceStatistics(
        units=stocks_balances,
        error_unit_ids=errors,
    )
