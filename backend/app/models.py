from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint
from .database import Base

class Worker(Base):
    __tablename__ = "workers"
    worker_id = Column(String, primary_key=True)
    name = Column(String)

class Workstation(Base):
    __tablename__ = "workstations"
    station_id = Column(String, primary_key=True)
    name = Column(String)

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    worker_id = Column(String, ForeignKey("workers.worker_id"))
    workstation_id = Column(String, ForeignKey("workstations.station_id"))
    event_type = Column(String)
    confidence = Column(Float)
    count = Column(Integer, default=0)

    __table_args__ = (
        UniqueConstraint("timestamp","worker_id","event_type", name="unique_event_constraint"),
    )