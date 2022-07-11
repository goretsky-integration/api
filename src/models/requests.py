from pydantic import BaseModel


class UnitIdAndName(BaseModel):
    id: int
    name: str
