from dataclasses import dataclass
from uuid import UUID

__all__ = (
    'UnitProductivityBalanceStatistics',
    'UnitRestaurantCookingTimeStatistics',
    'UnitHeatedShelfTimeStatistics',
)


@dataclass(frozen=True, slots=True)
class UnitProductivityBalanceStatistics:
    unit_uuid: UUID
    sales_per_labor_hour: int
    orders_per_labor_hour: float
    stop_sale_duration_in_seconds: int


@dataclass(frozen=True, slots=True)
class UnitRestaurantCookingTimeStatistics:
    unit_uuid: UUID
    average_tracking_pending_and_cooking_time: int


@dataclass(frozen=True, slots=True)
class UnitHeatedShelfTimeStatistics:
    unit_uuid: UUID
    average_heated_shelf_time: int = 0
