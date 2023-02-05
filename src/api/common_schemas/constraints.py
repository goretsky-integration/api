from enum import StrEnum, auto
from typing import TypeAlias
from uuid import UUID

from pydantic import conset, conlist, BaseModel

__all__ = (
    'CountryCode',
    'UnitIDs',
    'UnitUUIDs',
    'UnitIDsAndNames',
)


class CountryCode(StrEnum):
    RU = auto()
    BY = auto()
    CN = auto()
    CZ = auto()
    DE = auto()
    EE = auto()
    FI = auto()
    GB = auto()
    KG = auto()
    KZ = auto()
    LT = auto()
    NG = auto()
    PL = auto()
    RO = auto()
    SI = auto()
    SK = auto()
    TJ = auto()
    UZ = auto()
    VN = auto()


class UnitIdAndNameIn(BaseModel):
    id: int
    name: str


UnitIDsAndNames: TypeAlias = conlist(UnitIdAndNameIn, min_items=1, max_items=30)
UnitUUIDs: TypeAlias = conset(UUID, min_items=1, max_items=30)
UnitIDs: TypeAlias = conset(int, min_items=1, max_items=30)
