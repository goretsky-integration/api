import models
import models.dodo_is_api.partial_statistics.kitchen


def kitchen_statistics_to_kitchen_performance(
        units_kitchen_statistics: models.UnitsKitchenPartialStatistics,
) -> models.KitchenPerformanceStatistics:
    units = [
        models.UnitKitchenPerformance(
            unit_id=unit_kitchen_statistics.unit_id,
            revenue_per_hour=unit_kitchen_statistics.revenue.per_hour,
            revenue_delta_from_week_before=unit_kitchen_statistics.revenue.delta_from_week_before,
        ) for unit_kitchen_statistics in units_kitchen_statistics.units
    ]
    return models.KitchenPerformanceStatistics(
        units=units,
        error_unit_ids=units_kitchen_statistics.error_unit_ids
    )


def kitchen_statistics_to_production_statistics(
        units_kitchen_statistics: models.UnitsKitchenPartialStatistics,
) -> models.KitchenProductionStatistics:
    units = [
        models.UnitKitchenProduction(
            unit_id=unit_kitchen_statistics.unit_id,
            average_cooking_time=unit_kitchen_statistics.average_cooking_time,
        ) for unit_kitchen_statistics in units_kitchen_statistics.units
    ]
    return models.KitchenProductionStatistics(
        units=units,
        error_unit_ids=units_kitchen_statistics.error_unit_ids
    )
