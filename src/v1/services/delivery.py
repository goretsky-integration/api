from typing import Iterable

import httpx

from v2.periods import Period

__all__ = ('get_delivery_statistics_excel',)


def get_delivery_statistics_excel(client: httpx.Client, unit_ids: Iterable[int], period: Period) -> bytes:
    request_data = {
        'unitsIds': tuple(unit_ids),
        'beginDate': period.start.strftime('%d.%m.%Y'),
        'endDate': period.end.strftime('%d.%m.%Y'),
    }
    response = client.post(
        url='https://officemanager.dodopizza.ru/Reports/DeliveryStatistic/Export',
        data=request_data,
    )
    return response.content
