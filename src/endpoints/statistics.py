from fastapi import APIRouter

import models
from services.convert_models import weekly_operational_statistics_to_revenue_statistics
from services.public_dodo_api import get_operational_statistics_for_today_and_week_before

router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.post(
    path='/revenue/{unit_id}',
    response_model=models.RevenueForTodayAndWeekBeforeStatistics,
)
async def revenue_for_today_and_week_before_statistics(unit_id: int):
    operational_statistics = await get_operational_statistics_for_today_and_week_before(unit_id)
    return weekly_operational_statistics_to_revenue_statistics(operational_statistics)
