from fastapi import Depends, HTTPException, Body, APIRouter

from repository.bus_stop import BusStopRepository
from schema.bus_stop import BusStopScheme, BusStopListScheme

router = APIRouter(prefix="/api/bus-stops")

@router.get("", status_code=200)
def get_bus_stops_handler(
        bus_stop_repo: BusStopRepository = Depends(),
) -> BusStopListScheme:
    busstops = bus_stop_repo.get_busstops()

    return BusStopListScheme(
        busstops=[BusStopScheme.from_orm(busstop) for busstop in busstops]
    )
