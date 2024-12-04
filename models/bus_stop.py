from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BusStop(Base):
    __tablename__ = "busstop"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    def __repr__(self):
        return f"BusStop(id={self.id}, name={self.name}, latitude={self.latitude}, longitude={self.longitude})"