import collections
from typing import TypeVar, Protocol, Iterable
from uuid import UUID


class ItemWithUnitUUID(Protocol):
    unit_uuid: UUID


T = TypeVar('T', bound=ItemWithUnitUUID)


def group_by_unit_uuid(stop_sales: Iterable[T]) -> dict[UUID, list[T]]:
    unit_uuid_to_stop_sales = collections.defaultdict(list)
    for stop_sale in stop_sales:
        unit_uuid_to_stop_sales[stop_sale.unit_uuid].append(stop_sale)
    return unit_uuid_to_stop_sales


def find_missing_unit_uuids(
        all_unit_uuids: Iterable[UUID],
        items_with_unit_uuid: Iterable[ItemWithUnitUUID],
) -> set[UUID]:
    return set(all_unit_uuids) - {item.unit_uuid for item in items_with_unit_uuid}
