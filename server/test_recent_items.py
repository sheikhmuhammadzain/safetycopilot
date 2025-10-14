"""
Test script to verify the recent items endpoints work correctly
Run this after starting your backend server.
"""

import requests
import json
from typing import List, Dict, Any

BASE_URL = "http://localhost:8000"

def test_endpoint(endpoint: str, name: str, expected_fields: List[str]) -> None:
    """Test a single endpoint and verify the response structure."""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"Endpoint: {endpoint}")
    print('='*60)
    
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            print("⚠️  WARNING: No data returned (empty list)")
            return
        
        print(f"✅ Success! Received {len(data)} items")
        
        # Verify fields
        print(f"\n📋 First item structure:")
        first_item = data[0]
        for field in expected_fields:
            if field in first_item:
                print(f"  ✓ {field}: {first_item[field]}")
            else:
                print(f"  ✗ MISSING: {field}")
        
        # Display all items
        print(f"\n📊 All items:")
        for i, item in enumerate(data, 1):
            print(f"  {i}. {item.get('id', 'NO-ID')} | {item.get('status', 'NO-STATUS')} | {item.get('date', 'NO-DATE')}")
            if 'title' in item and item['title']:
                title = item['title'][:60] + '...' if len(item['title']) > 60 else item['title']
                print(f"     Title: {title}")
        
        # Verify sorting (most recent first)
        dates = [item.get('date', '') for item in data if item.get('date')]
        if len(dates) >= 2:
            is_sorted = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
            if is_sorted:
                print(f"\n✅ Dates are correctly sorted (most recent first)")
            else:
                print(f"\n⚠️  WARNING: Dates may not be sorted correctly")
                print(f"   Dates: {dates}")
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to server. Is it running?")
        print("   Run: uvicorn app.main:app --reload --port 8000")
    except requests.exceptions.HTTPError as e:
        print(f"❌ HTTP ERROR: {e}")
        print(f"   Status Code: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")

def main():
    """Run all tests."""
    print("🧪 Testing Recent Items Endpoints")
    print("Make sure your backend server is running on http://localhost:8000")
    
    # Test Recent Incidents
    test_endpoint(
        "/data/incidents/recent?limit=5",
        "Recent Incidents",
        ["id", "title", "department", "status", "date"]
    )
    
    # Test Recent Hazards
    test_endpoint(
        "/data/hazards/recent?limit=5",
        "Recent Hazards",
        ["id", "title", "status", "date"]
    )
    
    # Test Recent Audits
    test_endpoint(
        "/data/audits/recent?limit=5",
        "Recent Audits",
        ["id", "title", "status", "date"]
    )
    
    # Test with different limits
    print(f"\n{'='*60}")
    print("Testing with different limits")
    print('='*60)
    
    for limit in [1, 3, 10]:
        try:
            response = requests.get(f"{BASE_URL}/data/incidents/recent?limit={limit}")
            data = response.json()
            print(f"✅ limit={limit}: Received {len(data)} items")
        except Exception as e:
            print(f"❌ limit={limit}: {e}")
    
    print(f"\n{'='*60}")
    print("✅ All tests completed!")
    print('='*60)
    print("\nNext steps:")
    print("1. Review the output above to verify data accuracy")
    print("2. Check that IDs match your Excel file format")
    print("3. Verify dates are in correct order (most recent first)")
    print("4. Integrate these endpoints into your frontend")

if __name__ == "__main__":
    main()
