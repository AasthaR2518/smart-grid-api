import os
import sys
import subprocess
import datetime
from typing import List

# Install dependencies if they are not present
try:
    import fastapi
    import uvicorn
except ImportError:
    print("Installing fastapi, uvicorn, and pydantic for local development fallback...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"])
    import fastapi
    import uvicorn

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Smart Grid Operations - Week 1 Local Mock Server",
    description="Local fallback server simulating TimescaleDB and FastAPI ingestion in memory."
)

# In-memory database
meters_db = {}          # meter_id -> zone_id
readings_db = []        # list of telemetry readings

# Schemas
class MeterCreate(BaseModel):
    id: str = Field(..., alias="Meter ID")
    zone_id: str = Field(..., alias="Zone ID")

class MeterReadingCreate(BaseModel):
    meter_id: str = Field(..., alias="Meter ID")
    voltage: float = Field(..., alias="Voltage", ge=0.0)
    current: float = Field(..., alias="Current", ge=0.0)
    time: str = Field(..., alias="Timestamp")

# Endpoints
@app.get("/")
def read_root():
    return {
        "service": "Smart Grid Ingestion Mock Server (Week 1 Setup)",
        "status": "online",
        "docs_url": "http://localhost:8001/docs"
    }

@app.post("/api/v1/meters", status_code=201)
def create_meter(meter: MeterCreate):
    m_id = meter.id
    if m_id in meters_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Meter with ID '{m_id}' is already registered."
        )
    meters_db[m_id] = meter.zone_id
    print(f"Registered meter: {m_id} in {meter.zone_id}")
    return {
        "Meter ID": m_id,
        "Zone ID": meter.zone_id,
        "created_at": datetime.datetime.now().isoformat()
    }

@app.get("/api/v1/meters")
def get_meters():
    return [
        {"Meter ID": m_id, "Zone ID": z_id, "created_at": datetime.datetime.now().isoformat()} 
        for m_id, z_id in meters_db.items()
    ]

@app.post("/api/v1/readings", status_code=201)
def create_reading(reading: MeterReadingCreate):
    if reading.meter_id not in meters_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Meter ID '{reading.meter_id}' is not registered."
        )
    readings_db.append(reading.model_dump(by_alias=True))
    print(f"Ingested telemetry readout: {reading.meter_id} | V: {reading.voltage}V | A: {reading.current}A")
    return {"status": "success"}

@app.post("/api/v1/readings/bulk", status_code=201)
def create_readings_bulk(readings: List[MeterReadingCreate]):
    for r in readings:
        if r.meter_id not in meters_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Meter ID '{r.meter_id}' is not registered."
            )
    for r in readings:
        readings_db.append(r.model_dump(by_alias=True))
    print(f"Ingested bulk telemetry: {len(readings)} readings.")
    return {"status": "success", "message": f"Processed {len(readings)} readings."}

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Smart Grid Mock Server on http://localhost:8001")
    print("=" * 60)
    uvicorn.run(app, host="127.0.0.1", port=8001)
