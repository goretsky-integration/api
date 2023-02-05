from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'UnitDeliveryProductivityStatistics',
    'UnitDeliverySpeedStatistics',
    'UnitLateDeliveryVouchers',
    'DeliveryPartialStatisticsReport',
    'UnitDeliveryPartialStatistics',
)


@dataclass(frozen=True, slots=True)
class UnitDeliverySpeedStatistics:
    unit_uuid: UUID
    average_cooking_time: int = 0
    average_delivery_order_fulfillment_time: int = 0
    average_heated_shelf_time: int = 0
    average_order_trip_time: int = 0


@dataclass(frozen=True, slots=True)
class UnitDeliveryProductivityStatistics:
    unit_uuid: UUID
    orders_per_courier_labour_hour_today: float = 0
    orders_per_courier_labour_hour_week_before: float = 0
    from_week_before_in_percents: int = 0


@dataclass(frozen=True, slots=True)
class UnitLateDeliveryVouchers:
    unit_uuid: UUID
    certificates_count_today: int
    certificates_count_week_before: int


@dataclass(frozen=True, slots=True)
class UnitDeliveryPartialStatistics:
    unit_id: int
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


@dataclass(frozen=True, slots=True)
class DeliveryPartialStatisticsReport:
    results: list[UnitDeliveryPartialStatistics]
    errors: list[int]