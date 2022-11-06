import uuid

from pydantic import constr, conset

__all__ = (
    'CountryCode',
    'UnitUUIDsIn',
)

CountryCode = constr(min_length=2, max_length=2, to_lower=True, strict=True)
UnitUUIDsIn = conset(uuid.UUID, min_items=1, max_items=30)
