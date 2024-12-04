from typing import List

from pydantic import BaseModel

from models.bus_stop import BusStop


class BusStopScheme(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float

    class Config:
        orm_mode = True

class BusStopListScheme(BaseModel):
    busStops: List[BusStop]