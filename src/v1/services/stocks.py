import httpx

from v1 import exceptions, parsers, models


async def get_stocks_balance(client: httpx.AsyncClient, unit_id: int | str) -> list[models.StockBalance]:
    url = 'https://officemanager.dodopizza.ru/OfficeManager/StockBalance/Get'
    params = {'unitId': unit_id}
    response = await client.get(url, params=params)
    if response.is_error:
        raise exceptions.UnitIDAPIError(unit_id=unit_id)
    return parsers.StockBalanceHTMLParser(response.text, unit_id).parse()
