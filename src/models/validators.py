from typing import TypeVar

__all__ = (
    'get_or_none',
)

T = TypeVar('T')


def get_or_none(value: T) -> T | None:
    return value or None
