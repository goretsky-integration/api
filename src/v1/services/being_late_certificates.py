from typing import Iterable

import httpx

from core import config
from v1 import models, parsers
from v2.periods import Period


def zip_certificates_today_and_week_before(
        units: Iterable[models.UnitIdAndNameIn],
        certificates_today: Iterable[models.UnitBeingLateCertificates],
        certificates_week_before: Iterable[models.UnitBeingLateCertificates],
) -> list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
    unit_id_to_count_today = {report.unit_id: report.certificates_count for report in certificates_today}
    unit_id_to_count_week_before = {report.unit_id: report.certificates_count for report in certificates_week_before}
    return [
        models.UnitBeingLateCertificatesTodayAndWeekBefore(
            unit_id=unit.id,
            unit_name=unit.name,
            certificates_count_today=unit_id_to_count_today.get(unit.id, 0),
            certificates_count_week_before=unit_id_to_count_week_before.get(unit.id, 0),
        ) for unit in units
    ]


async def get_being_late_certificates(
        cookies: dict,
        units: Iterable[models.UnitIdAndNameIn],
        period: Period,
) -> list[models.UnitBeingLateCertificates]:
    unit_ids = [unit.id for unit in units]
    url = 'https://officemanager.dodopizza.ru/Reports/BeingLateCertificates/Get'
    data = {
        'unitsIds': unit_ids,
        'beginDate': period.start.strftime('%d.%m.%Y'),
        'endDate': period.end.strftime('%d.%m.%Y'),
    }
    headers = {'User-Agent': config.APP_USER_AGENT}
    async with httpx.AsyncClient(cookies=cookies) as client:
        response = await client.post(url, data=data, headers=headers, timeout=30)
    return parsers.BeingLateCertificatesParser(response.text, unit_ids[0], units).parse()
