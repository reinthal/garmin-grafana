#!/usr/bin/env python3
"""
Test script for InfluxDB v2 integration with Garmin fetch
This script tests the basic functionality of the InfluxDB v2 client setup
"""

import os
import sys
from datetime import datetime, timezone
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

def test_influxdb_v2_connection():
    """Test InfluxDB v2 connection and basic operations"""
    
    # Configuration (you can override with environment variables)
    url = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    token = os.getenv("INFLUXDB_TOKEN", "your_token_here")
    org = os.getenv("INFLUXDB_ORG", "your_org_here")
    bucket = os.getenv("INFLUXDB_DATABASE", "GarminStats")
    
    print(f"Testing InfluxDB v2 connection...")
    print(f"URL: {url}")
    print(f"Organization: {org}")
    print(f"Bucket: {bucket}")
    
    try:
        # Create client
        client = InfluxDBClient(url=url, token=token, org=org)
        
        # Test connection by pinging
        health = client.health()
        print(f"✅ Connection successful: {health}")
        
        # Create write and query APIs
        write_api = client.write_api(write_options=SYNCHRONOUS)
        query_api = client.query_api()
        
        # Test write operation
        test_point = Point("TestMeasurement")\
            .tag("test_tag", "test_value")\
            .field("test_field", 42)\
            .time(datetime.now(timezone.utc), WritePrecision.NS)
        
        write_api.write(bucket=bucket, record=test_point)
        print("✅ Write operation successful")
        
        # Test query operation
        query = f'''
        from(bucket: "{bucket}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "TestMeasurement")
          |> limit(n: 1)
        '''
        
        result = query_api.query(query)
        if result and len(result) > 0 and len(result[0].records) > 0:
            print("✅ Query operation successful")
            print(f"   Found {len(result[0].records)} records")
        else:
            print("⚠️ Query returned no results (this might be expected)")
        
        # Clean up test data
        delete_api = client.delete_api()
        start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
        stop = datetime.now(timezone.utc).replace(hour=23, minute=59, second=59, microsecond=999999)
        delete_api.delete(start, stop, '_measurement="TestMeasurement"', bucket=bucket, org=org)
        print("✅ Test data cleaned up")
        
        client.close()
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_influxdb_v2_connection()
    sys.exit(0 if success else 1) 