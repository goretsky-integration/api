import asyncio
from typing import Iterable

from fastapi import APIRouter, Body, Depends

import models
from repositories import OfficeManagerRepository, get_office_manager_repository
from utils import exceptions

router = APIRouter(prefix='/stocks')


def filter_stocks_balance_by_days_left(
        stocks_balance: Iterable[models.StockBalance],
        days_left_threshold: int,
) -> list[models.StockBalance]:
    return [stock_balance for stock_balance in stocks_balance if stock_balance.days_left <= days_left_threshold]


@router.post(
    path='/',
    response_model=models.StockBalanceStatistics,
)
async def get_ingredient_stocks(
        unit_ids: set[int] = Body(),
        cookies: dict[str, str] = Body(),
        days_left_threshold: int | None = Body(default=None),
        office_manager: OfficeManagerRepository = Depends(get_office_manager_repository),
):
    async with office_manager:
        tasks = (office_manager.get_stocks_balance(cookies, unit_id) for unit_id in unit_ids)
        responses: tuple[list[models.StockBalance] | exceptions.StocksBalanceAPIError, ...] = await asyncio.gather(
            *tasks, return_exceptions=True)
    error_unit_ids: list[int] = []
    units: list[models.StockBalance] = []
    for units_responses in responses:
        if isinstance(units_responses, exceptions.StocksBalanceAPIError):
            error_unit_ids.append(units_responses.unit_id)
        else:
            if days_left_threshold is not None:
                units_responses = filter_stocks_balance_by_days_left(units_responses, days_left_threshold)
            units += units_responses
    return models.StockBalanceStatistics(units=units, error_unit_ids=error_unit_ids)
