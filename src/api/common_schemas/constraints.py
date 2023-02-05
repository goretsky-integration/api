from enum import Enum
from typing import TypeAlias
from uuid import UUID

from pydantic import conset, conlist, BaseModel

__all__ = (
    'CountryCode',
    'UnitIDs',
    'UnitUUIDs',
    'UnitIDsAndNames',
)


class CountryCode(Enum):
    RU = 'ru'
    BY = 'by'
    CN = 'cn'
    CZ = 'cz'
    DE = 'de'
    EE = 'ee'
    FI = 'fi'
    GB = 'gb'
    KG = 'kg'
    KZ = 'kz'
    LT = 'lt'
    NG = 'ng'
    PL = 'pl'
    RO = 'ro'
    SI = 'si'
    SK = 'sk'
    TJ = 'tj'
    UZ = 'uz'
    VN = 'vn'


class UnitIdAndNameIn(BaseModel):
    id: int
    name: str


UnitIDsAndNames: TypeAlias = conlist(UnitIdAndNameIn, min_items=1, max_items=30)
UnitUUIDs: TypeAlias = conset(UUID, min_items=1, max_items=30)
UnitIDs: TypeAlias = conset(int, min_items=1, max_items=30)
