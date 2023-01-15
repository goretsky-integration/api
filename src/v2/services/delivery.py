import collections
from typing import Iterable
from uuid import UUID

from v2 import models

__all__ = ('count_late_delivery_vouchers',)


def count_late_delivery_vouchers(
        vouchers: Iterable[models.LateDeliveryVoucher],
) -> dict[UUID, int]:
    unit_uuid_to_vouchers_count = collections.defaultdict(int)
    for voucher in vouchers:
        unit_uuid_to_vouchers_count[voucher.unit_uuid] += 1
    return unit_uuid_to_vouchers_count
