import asyncio
from datetime import timedelta
from typing import Iterable

import models
from services.api import dodo_is_api
from utils import time_utils

BeingLateCertificatesBatch = models.SingleUnitBeingLateCertificates | list[models.UnitBeingLateCertificates]


def zip_certificates_today_and_week_before(
        certificates_today: Iterable[models.UnitBeingLateCertificates],
        certificates_week_before: Iterable[models.UnitBeingLateCertificates],
) -> list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
    certificates_today_unit_name_to_count = {report.unit_name: report.being_late_certificates_count
                                             for report in certificates_today}
    certificates_week_before_unit_name_to_count = {report.unit_name: report.being_late_certificates_count
                                                   for report in certificates_week_before}
    all_unit_names = set(certificates_today_unit_name_to_count) | set(certificates_week_before_unit_name_to_count)

    result = []
    for unit_name in all_unit_names:
        certificates_today_count = certificates_today_unit_name_to_count.get(unit_name, 0)
        certificates_week_before_count = certificates_week_before_unit_name_to_count.get(unit_name, 0)
        result.append(models.UnitBeingLateCertificatesTodayAndWeekBefore(
            unit_name=unit_name,
            certificates_today_count=certificates_today_count,
            certificates_week_before_count=certificates_week_before_count,
        ))
    return result


async def get_being_late_certificates_statistics(
        cookies: dict,
        unit_ids: Iterable[int],
) -> models.SingleUnitBeingLateCertificatesTodayAndWeekBefore \
     | list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
    today = time_utils.get_moscow_datetime_now()
    week_before = today - timedelta(days=7)

    task_today = dodo_is_api.get_being_late_certificates(cookies, unit_ids, today, today)
    task_week_before = dodo_is_api.get_being_late_certificates(cookies, unit_ids, week_before, week_before)
    responses: tuple[BeingLateCertificatesBatch, ...] = await asyncio.gather(task_today, task_week_before)
    certificates_today, certificates_week_before = responses

    if isinstance(certificates_today, models.SingleUnitBeingLateCertificates):
        return models.SingleUnitBeingLateCertificatesTodayAndWeekBefore(
            certificates_today_count=certificates_today.being_late_certificates_count,
            certificates_week_before_count=certificates_week_before.being_late_certificates_count,
        )
    return zip_certificates_today_and_week_before(certificates_today, certificates_week_before)
