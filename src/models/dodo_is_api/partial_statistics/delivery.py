from pydantic import BaseModel

__all__ = (
    'DeliveryWorkPartial',
    'UnitsDeliveryPartialStatistics',
)


class Performance(BaseModel):
    orders_for_courier_count_per_hour_today: float
    orders_for_courier_count_per_hour_week_before: float
    delta_from_week_before: int


class HeatedShelf(BaseModel):
    orders_count: int
    orders_awaiting_time: int


class Couriers(BaseModel):
    in_queue_count: int
    total_count: int


class DeliveryWorkPartial(BaseModel):
    unit_id: int
    performance: Performance
    heated_shelf: HeatedShelf
    couriers: Couriers


class UnitsDeliveryPartialStatistics(BaseModel):
    units: list[DeliveryWorkPartial]
    error_unit_ids: list[int]
