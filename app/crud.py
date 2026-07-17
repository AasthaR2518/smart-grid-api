from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas

# Meter Operations
async def get_meter(db: AsyncSession, meter_id: str):
    result = await db.execute(select(models.Meter).where(models.Meter.id == meter_id))
    return result.scalars().first()

async def create_meter(db: AsyncSession, meter: schemas.MeterCreate):
    db_meter = models.Meter(id=meter.id, zone_id=meter.zone_id)
    db.add(db_meter)
    await db.commit()
    await db.refresh(db_meter)
    return db_meter

async def get_meters(db: AsyncSession, skip: int = 0, limit: int = 100):
    result = await db.execute(select(models.Meter).offset(skip).limit(limit))
    return result.scalars().all()

# Reading Operations
async def create_meter_reading(db: AsyncSession, reading: schemas.MeterReadingCreate):
    db_reading = models.MeterReading(
        time=reading.time,
        meter_id=reading.meter_id,
        voltage=reading.voltage,
        current=reading.current
    )
    db.add(db_reading)
    await db.commit()
    return db_reading

async def create_meter_readings_bulk(db: AsyncSession, readings: list[schemas.MeterReadingCreate]):
    db_readings = [
        models.MeterReading(
            time=r.time,
            meter_id=r.meter_id,
            voltage=r.voltage,
            current=r.current
        )
        for r in readings
    ]
    db.add_all(db_readings)
    await db.commit()
    return db_readings
