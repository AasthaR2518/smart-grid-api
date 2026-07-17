from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.database import get_async_db
from app import schemas, crud

app = FastAPI(
    title="Smart Grid Load Balancing & Forecasting API",
    description="High-performance backend for real-time electrical grid telemetry ingestion (Week 1 Scope).",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {
        "service": "Smart Grid Operations Center API (Week 1 Setup)",
        "status": "online",
        "docs_url": "/docs"
    }

# ----------------- Meter Management Endpoints -----------------

@app.post("/api/v1/meters", response_model=schemas.MeterResponse, status_code=status.HTTP_201_CREATED)
async def create_meter(meter: schemas.MeterCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Register a new smart meter.
    Meters must be registered before sending telemetry.
    """
    db_meter = await crud.get_meter(db, meter_id=meter.id)
    if db_meter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Meter with ID '{meter.id}' is already registered."
        )
    return await crud.create_meter(db, meter)

@app.get("/api/v1/meters", response_model=List[schemas.MeterResponse])
async def get_meters(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_async_db)):
    """
    Get a list of all registered smart meters.
    """
    return await crud.get_meters(db, skip=skip, limit=limit)

# ----------------- Telemetry Ingestion Endpoints -----------------

@app.post("/api/v1/readings", status_code=status.HTTP_201_CREATED)
async def create_reading(reading: schemas.MeterReadingCreate, db: AsyncSession = Depends(get_async_db)):
    """
    Ingest a single smart meter telemetry reading (Voltage, Current, Timestamp, Meter ID).
    Raises 400 Bad Request if the Meter ID is not registered.
    """
    try:
        await crud.create_meter_reading(db, reading)
        return {"status": "success", "message": "Telemetry reading ingested."}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Meter ID '{reading.meter_id}' is not registered. Please register the meter first."
        )

@app.post("/api/v1/readings/bulk", status_code=status.HTTP_201_CREATED)
async def create_readings_bulk(readings: List[schemas.MeterReadingCreate], db: AsyncSession = Depends(get_async_db)):
    """
    Ingest a batch of smart meter telemetry readings for high-throughput batching.
    """
    if not readings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Readings list cannot be empty."
        )
    try:
        await crud.create_meter_readings_bulk(db, readings)
        return {"status": "success", "message": f"{len(readings)} telemetry readings ingested."}
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more readings reference unregistered meters. Ensure all meters are registered first."
        )
