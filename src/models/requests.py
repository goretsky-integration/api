from pydantic import BaseModel

__all__ = (
    'CookiesAndUnitIds',
    'CookiesAndUnitId',
)


class CookiesAndUnitId(BaseModel):
    cookies: dict
    unit_id: int


class CookiesAndUnitIds(BaseModel):
    cookies: dict
    unit_ids: int
