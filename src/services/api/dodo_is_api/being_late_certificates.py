from typing import Iterable

import httpx

import models
from core import config
from services import parsers
from utils import time_utils

__all__ = (
    'get_being_late_certificates',
)


async def get_being_late_certificates(
        cookies: dict,
        units: Iterable[models.UnitIdAndName],
        datetime_config: time_utils.Period,
) -> list[models.UnitBeingLateCertificates]:
    unit_ids = [unit.id for unit in units]
    url = 'https://officemanager.dodopizza.ru/Reports/BeingLateCertificates/Get'
    data = {
        'unitsIds': unit_ids,
        'beginDate': datetime_config.from_datetime.strftime('%d.%m.%Y'),
        'endDate': datetime_config.to_datetime.strftime('%d.%m.%Y'),
    }
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, data=data, headers=headers, timeout=30)
    return parsers.BeingLateCertificatesParser(response.text, unit_ids[0], units).parse()
