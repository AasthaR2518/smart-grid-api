-- Enable TimescaleDB extension
CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

-- Create meters metadata table
CREATE TABLE IF NOT EXISTS meters (
    id VARCHAR(50) PRIMARY KEY,
    zone_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index on zone_id for faster queries
CREATE INDEX IF NOT EXISTS idx_meters_zone_id ON meters(zone_id);

-- Create meter_readings table
CREATE TABLE IF NOT EXISTS meter_readings (
    time TIMESTAMPTZ NOT NULL,
    meter_id VARCHAR(50) NOT NULL,
    voltage DOUBLE PRECISION NOT NULL,
    current DOUBLE PRECISION NOT NULL
);

-- Convert meter_readings to a hypertable partitioned by the 'time' column
SELECT create_hypertable('meter_readings', 'time', if_not_exists => TRUE);

-- Create index for quick readouts lookups per meter
CREATE INDEX IF NOT EXISTS idx_meter_readings_meter_time ON meter_readings(meter_id, time DESC);
