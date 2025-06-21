# InfluxDB v2 Support Implementation

This document outlines the changes made to add InfluxDB v2 support to the Garmin Grafana project.

## Overview

The project now supports three InfluxDB versions:
- **InfluxDB 1.11** (default, recommended)
- **InfluxDB 2.x** (newly added)
- **InfluxDB 3.x** (existing support)

## Changes Made

### 1. Dependencies

**File: `pyproject.toml`**
- Added `influxdb-client==1.40.0` dependency for InfluxDB v2 support

### 2. Main Application (`garmin_fetch.py`)

**Imports:**
- Added `from influxdb_client import InfluxDBClient as InfluxDBClient2, Point, WritePrecision`
- Added `from influxdb_client.client.write_api import SYNCHRONOUS`

**Configuration:**
- Updated version validation to accept '1', '2', '3'
- Added InfluxDB v2 environment variables:
  - `INFLUXDB_V2_TOKEN` (maps to `INFLUXDB_TOKEN`)
  - `INFLUXDB_V2_ORG` (maps to `INFLUXDB_ORG`)

**Connection Logic:**
- Added InfluxDB v2 client initialization for both HTTP and HTTPS
- Created separate `write_api` and `query_api` instances for v2

**Data Writing:**
- Updated `write_points_to_influxdb()` function to convert points to InfluxDB v2 format
- Uses `Point` objects with tags, fields, and timestamps
- Writes to bucket instead of database

**Data Querying:**
- Updated last sync time query to use Flux query language
- Uses `query_api.query()` with Flux syntax

### 3. Exporter (`influxdb_exporter.py`)

**Imports:**
- Added `from influxdb_client import InfluxDBClient as InfluxDBClient2`

**Configuration:**
- Updated version validation and added v2 environment variables

**Connection Logic:**
- Added InfluxDB v2 client initialization
- Created `query_api` instance for v2

**Data Export:**
- Updated measurements query to use Flux schema query
- Updated data querying to use Flux syntax with proper pivoting

### 4. Documentation

**README.md:**
- Updated InfluxDB version section to document v2 support
- Added configuration examples for all three versions
- Updated recommendations and limitations

**Compose Files:**
- Updated `compose-example.yml` with v2 configuration comments
- Created `compose-example-influxdb-v2.yml` as a complete v2 example

### 5. Testing

**Created `test_influxdb_v2.py`:**
- Basic connection test script
- Tests write and query operations
- Includes cleanup functionality

## Environment Variables

### InfluxDB v2 Required Variables

```bash
INFLUXDB_VERSION=2
INFLUXDB_HOST=your_influxdb_host
INFLUXDB_PORT=8086
INFLUXDB_DATABASE=GarminStats  # This becomes the bucket name
INFLUXDB_TOKEN=your_access_token
INFLUXDB_ORG=your_organization_name
```

### Optional Variables

```bash
INFLUXDB_ENDPOINT_IS_HTTP=True  # Set to False for HTTPS
```

## Usage Examples

### Docker Compose (v2)

```yaml
services:
  garmin-fetch-data:
    environment:
      - INFLUXDB_VERSION=2
      - INFLUXDB_HOST=influxdb
      - INFLUXDB_PORT=8086
      - INFLUXDB_DATABASE=GarminStats
      - INFLUXDB_TOKEN=your_token_here
      - INFLUXDB_ORG=your_org_here

  influxdb:
    image: 'influxdb:2.7'
    environment:
      - DOCKER_INFLUXDB_INIT_MODE=setup
      - DOCKER_INFLUXDB_INIT_USERNAME=admin
      - DOCKER_INFLUXDB_INIT_PASSWORD=adminpassword
      - DOCKER_INFLUXDB_INIT_ORG=your_org_here
      - DOCKER_INFLUXDB_INIT_BUCKET=GarminStats
      - DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=your_token_here
```

### Manual Testing

```bash
# Set environment variables
export INFLUXDB_URL="http://localhost:8086"
export INFLUXDB_TOKEN="your_token"
export INFLUXDB_ORG="your_org"
export INFLUXDB_DATABASE="GarminStats"

# Run test script
python test_influxdb_v2.py
```

## Key Differences from v1

1. **Authentication**: Uses tokens instead of username/password
2. **Data Model**: Uses buckets instead of databases
3. **Query Language**: Uses Flux instead of InfluxQL
4. **Client API**: Different client library and API structure
5. **Point Format**: Uses `Point` objects instead of dictionaries

## Migration Notes

- Existing InfluxDB v1 users can continue using v1 without changes
- InfluxDB v2 users need to set `INFLUXDB_VERSION=2` and provide token/org
- Data format remains compatible across versions
- Grafana dashboards work with all versions (using appropriate query language)

## Testing

The implementation has been tested with:
- InfluxDB v2.7
- Basic write/query operations
- Data export functionality
- Connection handling for both HTTP and HTTPS

## Recommendations

- **For new users**: Use InfluxDB v1.11 (default) for best compatibility
- **For existing v2 users**: Use the new v2 support with `INFLUXDB_VERSION=2`
- **For production**: Consider v1.11 for better performance and Grafana compatibility 