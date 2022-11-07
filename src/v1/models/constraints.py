from pydantic import constr, conset, BaseModel, conlist

__all__ = (
    'CountryCode',
    'UnitIDsIn',
    'UnitIdAndNameIn',
    'UnitIdsAndNamesIn',
)

CountryCode = constr(min_length=2, max_length=2, to_lower=True, strict=True)
UnitIDsIn = conset(int, min_items=1, max_items=30)


class UnitIdAndNameIn(BaseModel):
    id: int
    name: str


UnitIdsAndNamesIn = conlist(UnitIdAndNameIn, min_items=1, max_items=30)
