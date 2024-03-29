from typing import AsyncGenerator
from uuid import UUID

from services.http_client_factories import AsyncHTTPClient
from models.external_api_responses import shift_manager as shift_manager_models
from services import parsers
from services.periods import Period

__all__ = ('ShiftManagerAPI',)


class ShiftManagerAPI:

    def __init__(self, client: AsyncHTTPClient):
        self.__client = client

    async def get_partial_canceled_orders(
            self, period: Period) -> AsyncGenerator[list[shift_manager_models.OrderPartial], None]:
        url = '/Managment/ShiftManagment/PartialShiftOrders'
        request_params = {
            'page': 1,
            'date': period.end.date().isoformat(),
            'orderStateFilter': 'Failure',
        }
        while True:
            response = await self.__client.get(url, params=request_params, timeout=30)
            orders = parsers.OrdersPartial(response.text).parse()
            yield orders
            if not orders:
                break
            request_params['page'] += 1

    async def get_order_detail(
            self,
            order_uuid: UUID,
            order_price: int,
            order_type: str,
    ) -> shift_manager_models.OrderByUUID:
        url = '/Managment/ShiftManagment/Order'
        request_params = {'orderUUId': order_uuid.hex}
        response = await self.__client.get(url, params=request_params, timeout=30)
        return parsers.OrderByUUIDParser(response.text, order_uuid, order_price, order_type).parse()
