from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Meter(Base):
    __tablename__ = "meters"

    id = Column(String(50), primary_key=True, index=True)
    zone_id = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class MeterReading(Base):
    __tablename__ = "meter_readings"

    # In SQLAlchemy, we need a primary key definition even though TimescaleDB
    # hypertables don't enforce one. A composite key on (time, meter_id) satisfies SQLAlchemy.
    time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    meter_id = Column(String(50), ForeignKey("meters.id"), primary_key=True, nullable=False)
    voltage = Column(Float, nullable=False)
    current = Column(Float, nullable=False)
