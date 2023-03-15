import asyncio
import os
from uuid import uuid4, UUID

from fastapi import APIRouter, Body, Depends, Query

from api import common_schemas
from api.v1 import schemas, dependencies
from services import parsers
from services.domain import sales as sales_services
from services.external_dodo_api import OfficeManagerAPI, ShiftManagerAPI
from services.external_dodo_api.export_service import ExportServiceAPI
from services.http_client_factories import AsyncHTTPClient, HTTPClient
from services.periods import Period

router = APIRouter(prefix='/v1/{country_code}', tags=['Orders'])


@router.post(
    path='/cheated-orders',
)
async def get_cheated_orders(
        units: common_schemas.UnitIDsAndNames = Body(),
        repeated_phone_number_count_threshold: int = Body(),
        closing_office_manager_api_client: AsyncHTTPClient = Depends(
            dependencies.get_closing_office_manager_api_client),
) -> list[schemas.CheatedOrders]:
    period = Period.today()
    unit_ids = [unit.id for unit in units]
    async with closing_office_manager_api_client as client:
        api = OfficeManagerAPI(client)
        orders = await api.get_restaurant_orders(unit_ids, period)
    return sales_services.restaurant_orders_to_cheated_orders(orders, repeated_phone_number_count_threshold)


@router.get(
    path='/canceled-orders',
)
async def get_canceled_orders(
        closing_shift_manager_api_client: AsyncHTTPClient = Depends(dependencies.get_closing_shift_manager_api_client),
) -> list[schemas.OrderByUUID]:
    period = Period.today()
    async with closing_shift_manager_api_client as client:
        tasks = []
        api = ShiftManagerAPI(client)
        async for orders in api.get_partial_canceled_orders(period):
            if not orders:
                break
            for order in orders:
                tasks.append(api.get_order_detail(order.uuid, order.price, order.type))
        return await asyncio.gather(*tasks)


@router.get(
    path='/used-promo-codes',
)
def get_used_promo_codes(
        unit_ids: set[int] = Query(),
        temp_file_id: UUID = Depends(uuid4),
        closing_export_service_api_client: HTTPClient = Depends(dependencies.get_closing_export_service_api_client),
) -> list[schemas.UsedPromoCode]:
    period = Period.today()
    with closing_export_service_api_client as client:
        api = ExportServiceAPI(client)
        excel_report_bytes = api.get_promo_codes_excel_report(period, unit_ids)
    with open(f'./used-promo-codes-{temp_file_id}.xlsx', 'wb') as file:
        file.write(excel_report_bytes)
    try:
        return parsers.UsedPromoCodesExcelParser(f'./used-promo-codes-{temp_file_id}.xlsx').parse()
    finally:
        os.unlink(f'./used-promo-codes-{temp_file_id}.xlsx')
