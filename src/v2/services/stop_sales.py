import collections
import uuid
from typing import Iterable, TypeVar

from v2 import models

T = TypeVar('T', bound=models.StopSale)


def group_by_unit_uuid(stop_sales: Iterable[T]) -> dict[uuid.UUID, list[T]]:
    unit_uuid_to_stop_sales = collections.defaultdict(list)
    for stop_sale in stop_sales:
        unit_uuid_to_stop_sales[stop_sale.unit_uuid].append(stop_sale)
    return unit_uuid_to_stop_sales
