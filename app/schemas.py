from pydantic import BaseModel, Field, ConfigDict
import datetime

# Meter Schemas
class MeterCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(..., alias="Meter ID")
    zone_id: str = Field(..., alias="Zone ID")

class MeterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    id: str = Field(..., alias="Meter ID")
    zone_id: str = Field(..., alias="Zone ID")
    created_at: datetime.datetime

# Meter Reading Schemas
class MeterReadingCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    meter_id: str = Field(..., alias="Meter ID")
    voltage: float = Field(..., alias="Voltage", ge=0.0)
    current: float = Field(..., alias="Current", ge=0.0)
    time: datetime.datetime = Field(..., alias="Timestamp")

class MeterReadingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    
    meter_id: str = Field(..., alias="Meter ID")
    voltage: float = Field(..., alias="Voltage")
    current: float = Field(..., alias="Current")
    time: datetime.datetime = Field(..., alias="Timestamp")
