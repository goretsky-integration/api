from typing import Iterable

import httpx

from services.periods import Period


class ExportServiceAPI:

    def __init__(self, http_client: httpx.Client):
        self.__http_client = http_client

    def get_promo_codes_excel_report(self, period: Period, unit_ids: Iterable[int]) -> bytes:
        url = '/Reports/PromoCodeUsed/Export'
        request_data = {
            'unitsIds': tuple(unit_ids),
            'OrderSources': (
                'Telephone',
                'Site',
                'Restaurant',
                'DefectOrder',
                'Mobile',
                'Pizzeria',
                'Aggregator',
                'Kiosk',
            ),
            'beginDate': period.start.strftime('%d.%m.%Y'),
            'endDate': period.end.strftime('%d.%m.%Y'),
            'orderTypes': ('Delivery', 'Pickup', 'Stationary'),
            'IsAllPromoCode': [True, False],
            'OnlyComposition': False,
            'promoCode': '',
            'filterType': '',
        }
        response = self.__http_client.post(url, data=request_data, cookies={'SelectedLanguage7': 'ru-RU'})
        return response.content
