from pydantic import BaseModel

__all__ = ('TripsWithOneOrder',)


class TripsWithOneOrder(BaseModel):
    unit_name: str
    percentage: float
