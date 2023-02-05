from dataclasses import dataclass

from pydantic import BaseModel

__all__ = ('TripsWithOneOrder', 'UnitDeliveryPartialStatistics')


class TripsWithOneOrder(BaseModel):
    unit_name: str
    percentage: float


class UnitDeliveryPartialStatistics(BaseModel):
    unit_id: int
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


@dataclass(frozen=True, slots=True)
class DeliveryPartialStatisticsReport:
    results: list[UnitDeliveryPartialStatistics]
    errors: list[int]
