from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.connection import get_db
from models.bus_stop import BusStop


class BusStopRepository:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_busstops(self) -> List[BusStop]:
        return list(self.session.scalars(select(BusStop)))