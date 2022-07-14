import uuid
from datetime import datetime

from pydantic import BaseModel, validator

from models.validators import get_or_none

__all__ = (
    'OrderPartial',
    'OrderByUUID',
)


class OrderPartial(BaseModel):
    uuid: uuid.UUID
    price: int
    number: str
    type: str


class OrderByUUID(BaseModel):
    unit_name: str
    created_at: datetime
    receipt_printed_at: datetime | None
    number: str
    type: str
    price: int
    uuid: uuid.UUID

    @validator(
        'receipt_printed_at',
        'created_at',
        pre=True,
    )
    def str_to_datetime(cls, value: str | None) -> datetime | None:
        if isinstance(value, str):
            return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
        return value

    _replace_empty_objects_with_none = validator(
        'receipt_printed_at',
        allow_reuse=True
    )(get_or_none)
