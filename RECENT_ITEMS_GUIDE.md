# Recent Items API Guide

## Overview
This guide explains how to accurately retrieve recent incidents, hazards, and audits from your Safety Copilot system based on your actual data structure.

## Data Structure Analysis

### Incident Sheet
- **Total Rows**: 2,596 (866 valid incidents with complete data)
- **Key Columns**:
  - `Incident Number`: Format "IN-YYYYMMDD-NNN" (e.g., "IN-20220405-001")
  - `Date of Occurrence`: Primary date for sorting recent incidents
  - `Date Reported`: Fallback date
  - `Date Entered`: Secondary fallback
  - `Status`: "Closed", "Open", etc.
  - `Title`: Incident description
  - `Department`: "Process - EDC / VCM", "PVC", etc.

### Hazard ID Sheet
- **Key Columns**:
  - Hazard identifier column (check for "hazard_id" or similar)
  - `Date Entered`: Primary date for sorting
  - `Date Reported`: Fallback date
  - Status column
  - `Worst Case Consequence Potential (Hazard ID)`: Severity levels (C0-C3)
  - `Incident Type(s)`: Categories like "No Loss / No Injury", "Site HSE Rules", etc.

### Audit Sheet
- **Key Columns**:
  - `audit_id` or similar identifier
  - `scheduled_date` or `start_date`: Primary date for sorting
  - `audit_status`: Status indicator
  - `audit_title`: Title/description

---

## New API Endpoints

### 1. Recent Incidents
```
GET /data/incidents/recent?limit=5
```

**Description**: Returns the most recent incidents sorted by `Date of Occurrence` (falls back to `Date Reported` or `Date Entered`).

**Query Parameters**:
- `limit` (optional, default: 5): Number of recent items to return

**Response Format**:
```json
[
  {
    "id": "IN-20220405-001",
    "title": "OVR catalyst loss",
    "department": "Process - EDC / VCM",
    "status": "Closed",
    "date": "2022-04-05"
  }
]
```

**Example Requests**:

PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/data/incidents/recent?limit=5" -Method GET
```

curl:
```bash
curl http://localhost:8000/data/incidents/recent?limit=5
```

Python:
```python
import requests
response = requests.get("http://localhost:8000/data/incidents/recent", params={"limit": 5})
incidents = response.json()
```

---

### 2. Recent Hazards
```
GET /data/hazards/recent?limit=5
```

**Description**: Returns the most recent hazards sorted by `Date Entered` or `Date Reported`.

**Response Format**:
```json
[
  {
    "id": "HAZ-001",
    "title": "Hazard description",
    "status": "IDENTIFIED",
    "date": "2023-05-15"
  }
]
```

**Example Requests**:

PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/data/hazards/recent?limit=5" -Method GET
```

curl:
```bash
curl http://localhost:8000/data/hazards/recent?limit=5
```

---

### 3. Recent Audits
```
GET /data/audits/recent?limit=5
```

**Description**: Returns the most recent audits sorted by `scheduled_date` or `start_date`.

**Response Format**:
```json
[
  {
    "id": "AUD-001",
    "title": "Annual Safety Audit",
    "status": "SCHEDULED",
    "date": "2024-01-15"
  }
]
```

**Example Requests**:

PowerShell:
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/data/audits/recent?limit=5" -Method GET
```

curl:
```bash
curl http://localhost:8000/data/audits/recent?limit=5
```

---

## Frontend Integration

### Using the Recent Items in Your React UI

Based on your current UI screenshot showing "Recent Incidents", "Recent Hazards", and "Recent Audits" sections:

```typescript
// Example React hook to fetch recent items
import { useEffect, useState } from 'react';

interface RecentItem {
  id: string;
  title: string;
  status: string;
  date: string;
  department?: string; // Only for incidents
}

export function useRecentIncidents(limit = 5) {
  const [incidents, setIncidents] = useState<RecentItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`/data/incidents/recent?limit=${limit}`)
      .then(res => res.json())
      .then(data => {
        setIncidents(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to fetch recent incidents:', err);
        setLoading(false);
      });
  }, [limit]);

  return { incidents, loading };
}

// Similar hooks for hazards and audits
export function useRecentHazards(limit = 5) { /* ... */ }
export function useRecentAudits(limit = 5) { /* ... */ }
```

### Display Component Example

```tsx
function RecentIncidentsCard() {
  const { incidents, loading } = useRecentIncidents(5);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="recent-incidents-card">
      <h2>Recent Incidents</h2>
      {incidents.map((incident) => (
        <div key={incident.id} className="record-item">
          <div className="record-id">{incident.id}</div>
          <div className="record-status">{incident.status}</div>
        </div>
      ))}
    </div>
  );
}
```

---

## How the Backend Works

### Sorting Logic

1. **Date Column Detection**: The endpoints automatically search for the most appropriate date column:
   - **Incidents**: `Date of Occurrence` → `Date Reported` → `Date Entered`
   - **Hazards**: `Date Entered` → `Date Reported` → `occurrence_date`
   - **Audits**: `scheduled_date` → `start_date`

2. **Date Conversion**: Converts date columns to datetime format using pandas

3. **Filtering**: Removes rows with null/invalid dates

4. **Sorting**: Sorts by date in descending order (most recent first)

5. **Limiting**: Returns only the top N items (default 5)

### Column Name Handling

The implementation handles multiple possible column name variations:
- Case-insensitive matching
- Multiple naming conventions (e.g., "Date of Occurrence" vs "occurrence_date")
- Fallback to alternative columns if primary column is missing

---

## Testing the Endpoints

### 1. Start Your Backend Server

```bash
cd server
uvicorn app.main:app --reload --port 8000
```

### 2. Test with curl

```bash
# Test recent incidents
curl http://localhost:8000/data/incidents/recent

# Test with custom limit
curl http://localhost:8000/data/incidents/recent?limit=10

# Test recent hazards
curl http://localhost:8000/data/hazards/recent

# Test recent audits
curl http://localhost:8000/data/audits/recent
```

### 3. Test with PowerShell

```powershell
# Recent incidents
$incidents = Invoke-RestMethod -Uri "http://localhost:8000/data/incidents/recent" -Method GET
$incidents | Format-Table

# Recent hazards
$hazards = Invoke-RestMethod -Uri "http://localhost:8000/data/hazards/recent" -Method GET
$hazards | Format-Table

# Recent audits
$audits = Invoke-RestMethod -Uri "http://localhost:8000/data/audits/recent" -Method GET
$audits | Format-Table
```

### 4. Verify Data Accuracy

Check that:
- ✅ IDs match your Excel data format (e.g., "IN-20220405-001")
- ✅ Dates are in ISO format (YYYY-MM-DD)
- ✅ Status values are correct ("Closed", "IDENTIFIED", "SCHEDULED")
- ✅ Items are sorted from most recent to oldest
- ✅ The correct number of items is returned (default 5)

---

## Expected Output Examples

### Recent Incidents Example
```json
[
  {
    "id": "IN-20230211-003",
    "title": "Minor Car Accident",
    "department": "Commercial",
    "status": "Closed",
    "date": "2023-02-11"
  },
  {
    "id": "IN-20230102-001",
    "title": "Agitator moved and hit the ladder while Poly-A vessel entry was in-progress at PVC-1",
    "department": "PVC",
    "status": "Closed",
    "date": "2023-01-02"
  },
  {
    "id": "IN-20220405-001",
    "title": "OVR catalyst loss",
    "department": "Process - EDC / VCM",
    "status": "Closed",
    "date": "2022-04-05"
  }
]
```

### Recent Hazards Example
```json
[
  {
    "id": "HAZ-005",
    "title": "Safety violation identified during inspection",
    "status": "IDENTIFIED",
    "date": "2023-05-20"
  },
  {
    "id": "HAZ-004",
    "title": "Equipment failure risk",
    "status": "IDENTIFIED",
    "date": "2023-05-15"
  }
]
```

### Recent Audits Example
```json
[
  {
    "id": "AUD-005",
    "title": "Q2 Safety Compliance Audit",
    "status": "SCHEDULED",
    "date": "2024-06-01"
  },
  {
    "id": "AUD-004",
    "title": "Environmental Impact Assessment",
    "status": "SCHEDULED",
    "date": "2024-05-15"
  }
]
```

---

## Troubleshooting

### Issue: Empty Results
**Cause**: No valid date columns found or all dates are null
**Solution**: Check your Excel file to ensure date columns exist and have data

### Issue: Wrong Sort Order
**Cause**: Date column not properly converted to datetime
**Solution**: The endpoint automatically handles this, but verify your Excel dates are in a valid format

### Issue: Missing IDs
**Cause**: ID column not found in data
**Solution**: The endpoint generates fallback IDs (INC-001, HAZ-001, AUD-001) if no ID column exists

### Issue: Status Shows as Empty
**Cause**: Status column missing or has null values
**Solution**: Default statuses are provided:
- Incidents: "CLOSED"
- Hazards: "IDENTIFIED"
- Audits: "SCHEDULED"

---

## Next Steps

1. **Start your backend server** and test the endpoints
2. **Verify the data** matches your Excel file
3. **Integrate into your frontend** using the React hooks provided
4. **Customize the UI** to match your design requirements
5. **Add filtering options** if needed (by department, status, etc.)

For additional customization or questions, refer to the main project documentation or the backend code at `server/app/routers/data.py`.
