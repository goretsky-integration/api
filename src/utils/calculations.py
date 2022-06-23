__all__ = (
    'calculate_revenue_delta_in_percents',
    'calculate_proportion',
)


def calculate_proportion(
        *,
        x1: int | float,
        y1: int | float,
        x2: int | float,
) -> float:
    """Calculate proportion (unknown y2).
    x1   x2
    -- = --
    y1   y2
    Then y2 = (x2 * y1) / x1.

    Args:
        x1: Numerator of known ratio.
        y1: Denominator of known ratio.
        x2: Numerator of unknown ratio.

    Returns:
        Value of y2, i.e. denominator of unknown ratio.

    Examples:
        >>> print(calculate_proportion(x1=2, y1=4, x2=3))
        6
        >>> print(calculate_proportion(x1=15, y1=45, x2=60))
        180

    Raises:
        ValueError: if any of arguments equal to zero.
    """
    for num in (x1, y1, x2):
        if num == 0:
            raise ValueError('All parts of proportion must not be zero')
    return x2 * y1 / x1


def calculate_revenue_delta_in_percents(revenue_today: int | float,
                                        revenue_week_before: int | float) -> int:
    """Calculate how revenue has changed since week before.
    If either *revenue_today* or *revenue_week_before* equals to zero, zero will be returned.

    Args:
        revenue_today: Today's revenue.
        revenue_week_before: Revenue week before.

    Returns: Difference of revenue between today and week before in percents.
    """
    try:
        revenue_today_percents = round(calculate_proportion(
            x1=revenue_week_before,
            y1=100,
            x2=revenue_today,
        ))
        return revenue_today_percents - 100
    except ValueError:
        return 0


def calculate_orders_percentage_with_phone_numbers(
        orders_with_phone_numbers_count: int,
        total_orders_count: int,
) -> int:
    """
    Examples:
        >>> calculate_orders_percentage_with_phone_numbers(10, 40)
        25
        >>> calculate_orders_percentage_with_phone_numbers(0, 0)
        0

    Returns:
        Orders with phone numbers percentage.
    """
    try:
        return round(calculate_proportion(
            x1=total_orders_count,
            y1=100,
            x2=orders_with_phone_numbers_count,
        ))
    except ValueError:
        return 0
