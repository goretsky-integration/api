from pydantic import BaseModel


class UnitIdAndName(BaseModel):
    unit_id: int
    unit_name: str
