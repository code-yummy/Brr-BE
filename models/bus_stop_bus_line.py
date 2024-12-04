from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BusStopBusLine(Base):
    __tablename__ = "busstop_busline"

    id = Column(Integer, primary_key=True, index=True)
    bus_stop = relationship("BusStop", lazy="joined")
    bus_line = relationship("BusLine", lazy="joined")

    def __repr__(self):
        return f"BusStopBusLine(id={self.id}, bus_stop={self.bus_stop}, bus_line={self.bus_line})"