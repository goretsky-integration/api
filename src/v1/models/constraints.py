from pydantic import constr, conset

__all__ = (
    'CountryCode',
    'UnitIDsIn',
)

CountryCode = constr(min_length=2, max_length=2, to_lower=True, strict=True)
UnitIDsIn = conset(int, min_items=1, max_items=30)
