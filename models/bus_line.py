from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BusLine(Base):
    __tablename__ = "busline"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)

    def __repr__(self):
        return f"BusStop(id={self.id}, name={self.name})"