from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'UnitDeliveryProductivityStatistics',
    'UnitDeliverySpeedStatistics',
    'UnitLateDeliveryVouchers',
    'UnitLateDeliveryVouchersTodayAndWeekBefore',
)


@dataclass(frozen=True, slots=True)
class UnitDeliverySpeedStatistics:
    unit_uuid: UUID
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int


@dataclass(frozen=True, slots=True)
class UnitDeliveryProductivityStatistics:
    unit_uuid: UUID
    orders_per_courier_labour_hour_today: float
    orders_per_courier_labour_hour_week_before: float
    from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class UnitLateDeliveryVouchers:
    unit_uuid: UUID
    certificates_count_today: int
    certificates_count_week_before: int


@dataclass(frozen=True, slots=True)
class UnitLateDeliveryVouchersTodayAndWeekBefore:
    unit_uuid: UUID
    certificates_count_today: int
    certificates_count_week_before: int
