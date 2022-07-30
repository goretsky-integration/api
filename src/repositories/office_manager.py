import models
from services import parsers
from repositories.base import APIClientRepository

__all__ = (
    'OfficeManagerRepository',
)

from utils import exceptions


class OfficeManagerRepository(APIClientRepository):

    async def get_stocks_balance(self, cookies: dict[str, str], unit_id: int | str) -> list[models.StockBalance]:
        url = '/OfficeManager/StockBalance/Get'
        params = {'unitId': unit_id}
        response = await self._client.get(url, params=params, cookies=cookies)
        if response.is_server_error:
            raise exceptions.StocksBalanceAPIError(unit_id=unit_id)
        return parsers.StockBalanceHTMLParser(response.text, unit_id).parse()
