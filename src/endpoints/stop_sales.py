import uuid
from datetime import datetime

from fastapi import APIRouter, Query

from services.api import private_dodo_api

router = APIRouter(prefix='/stop-sales', tags=['Stop sales'])


@router.get(
    path='/ingredients',
    response_model_by_alias=False,
)
async def get_ingredient_stop_sales(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
        from_datetime: datetime | None = Query(None, description='Today unless specified'),
        to_datetime: datetime | None = Query(None, description='Current datetime unless specified'),
):
    return await private_dodo_api.get_ingredient_stop_sales(token, unit_uuids, from_datetime, to_datetime)


@router.get(
    path='/channels',
    response_model_by_alias=False,
)
async def get_channels_stop_sales(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
        from_datetime: datetime | None = Query(None, description='Today unless specified'),
        to_datetime: datetime | None = Query(None, description='Current datetime unless specified'),
):
    return await private_dodo_api.get_channels_stop_sales(token, unit_uuids, from_datetime, to_datetime)


@router.get(
    path='/products',
    response_model_by_alias=False,
)
async def get_products_stop_sales(
        token: str,
        unit_uuids: list[uuid.UUID] = Query(...),
        from_datetime: datetime | None = Query(None, description='Today unless specified'),
        to_datetime: datetime | None = Query(None, description='Current datetime unless specified'),
):
    return await private_dodo_api.get_products_stop_sales(token, unit_uuids, from_datetime, to_datetime)
