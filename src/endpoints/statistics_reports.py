from fastapi import APIRouter

import models

__all__ = (
    'router',
)

router = APIRouter(prefix='/v1/statistics', tags=['Statistics'])


@router.get(
    path='/productivity-balance/',
    response_model=models.ProductivityBalanceStatistics,
)
async def get_productivity_balance():
    return
