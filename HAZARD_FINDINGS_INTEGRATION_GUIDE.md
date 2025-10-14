# Hazard Top Findings Integration Guide

## 📋 Overview

This guide documents the implementation of the updated "Top Hazard Findings" chart that now shows **Incident Type Categories** with their counts instead of text descriptions.

## ✅ Test Results

### Backend Test (Completed Successfully)

```bash
cd server
python test_hazard_findings.py
```

**Results:**
- ✅ Loaded 1,211 hazard records with 169 columns
- ✅ Found 'Incident Type(s)' column
- ✅ Cleaned data: 994 valid entries (217 were null/empty)
- ✅ Identified 50 unique incident type categories

**Top Categories:**
1. No Loss / No Injury - 292 hazards (29.4%)
2. Site HSE Rules - 276 hazards (27.8%)
3. Other - 98 hazards (9.9%)
4. Site HSE Rules; No Loss / No Injury - 84 hazards (8.5%)
5. Injury - 57 hazards (5.7%)

**Distribution:**
- Categories with >100 hazards: 2
- Categories with 50-100 hazards: 4
- Categories with 10-49 hazards: 2
- Categories with 2-9 hazards: 20
- Categories with 1 hazard: 22
- Combined categories (with semicolons): 37

---

## 🔧 Backend Changes

### File: `server/app/routers/analytics_general.py`

#### Updated Endpoint (Line 876-942)

```python
@router.get("/data/hazard-top-findings")
async def data_hazard_top_findings(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    departments: Optional[List[str]] = Query(None),
    locations: Optional[List[str]] = Query(None),
    sublocations: Optional[List[str]] = Query(None),
    statuses: Optional[List[str]] = Query(None),
    violation_types: Optional[List[str]] = Query(None),
):
    """
    Returns hazard counts grouped by Incident Type(s).
    Shows category breakdown similar to: 'No Loss / No Injury', 'Site HSE Rules', etc.
    """
    df = get_hazard_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Apply filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, sublocations=sublocations, statuses=statuses,
        violation_types=violation_types
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Look for 'Incident Type(s)' column
    col_candidates = [
        "incident_type(s)",
        "incident type(s)",
        "incident_types",
        "incident type",
        "incident_type"
    ]
    col = _resolve_column(df, col_candidates)
    
    if col is None:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Clean the column: normalize whitespace, remove NA values
    series = (
        df[col]
        .astype(str)
        .str.replace("\xa0", " ", regex=False)  # Replace non-breaking spaces
        .str.replace(r"\s+", " ", regex=True)   # Normalize whitespace
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA, "null": pd.NA, "NULL": pd.NA})
        .dropna()
    )
    
    if series.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Count occurrences of each incident type category
    vc = series.value_counts().sort_values(ascending=False)
    
    # Return all categories (no limit)
    labels = [str(x) for x in vc.index.tolist()]
    counts = vc.values.astype(int).tolist()
    
    return JSONResponse(content={
        "labels": labels,
        "series": [{"name": "Hazards", "data": counts}],
    })
```

### Key Changes:
1. ✅ Now focuses on `Incident Type(s)` column instead of `description`
2. ✅ Removes all NA/null/empty values
3. ✅ Normalizes whitespace and non-breaking spaces
4. ✅ Returns ALL categories (no 20-item limit)
5. ✅ Series name changed from "Count" to "Hazards"

---

## 🚀 How to Start the Server

### Option 1: Development Mode (with auto-reload)

```bash
cd server
uvicorn app.main:app --reload --port 8000
```

### Option 2: Production Mode

```bash
cd server
uvicorn app.main:app --port 8000
```

### Verify Server is Running

```bash
# Check health endpoint
curl http://localhost:8000/health

# Test hazard findings endpoint
curl http://localhost:8000/analytics/data/hazard-top-findings
```

---

## 🧪 Testing the API Endpoint

### Method 1: Using curl (PowerShell)

```powershell
# Basic request
curl http://localhost:8000/analytics/data/hazard-top-findings

# With filters
curl "http://localhost:8000/analytics/data/hazard-top-findings?start_date=2023-01-01&end_date=2023-12-31"

# With department filter
curl "http://localhost:8000/analytics/data/hazard-top-findings?departments=HPO&departments=PVC"
```

### Method 2: Using Python

```python
import requests
import json

# Basic request
response = requests.get("http://localhost:8000/analytics/data/hazard-top-findings")
data = response.json()

print(f"Found {len(data['labels'])} categories")
print(f"\nTop 5 categories:")
for i in range(min(5, len(data['labels']))):
    print(f"  {i+1}. {data['labels'][i]}: {data['series'][0]['data'][i]} hazards")

# With filters
params = {
    "start_date": "2023-03-01",
    "end_date": "2023-12-31",
    "departments": ["HPO", "PVC"]
}
response = requests.get(
    "http://localhost:8000/analytics/data/hazard-top-findings",
    params=params
)
```

### Method 3: Using Browser

Open: http://localhost:8000/analytics/data/hazard-top-findings

Expected response:
```json
{
  "labels": [
    "No Loss / No Injury",
    "Site HSE Rules",
    "Other",
    "Site HSE Rules; No Loss / No Injury",
    "Injury",
    ...
  ],
  "series": [
    {
      "name": "Hazards",
      "data": [292, 276, 98, 84, 57, ...]
    }
  ]
}
```

---

## 🎨 Frontend Integration

The frontend already has the chart component configured. No changes needed!

### Current Implementation

**File:** `client/src/pages/Overview.tsx` (Line 855)

```tsx
<ShadcnBarCard 
    title="Top Hazard Findings" 
    endpoint="/analytics/data/hazard-top-findings" 
    params={{ dataset: "hazard", ...filterParams }} 
    refreshKey={refreshKey} 
/>
```

### How the Frontend Works:

1. **Component:** Uses `ShadcnBarCard` component
2. **Endpoint:** Calls `/analytics/data/hazard-top-findings`
3. **Filters:** Automatically applies global filters (date, department, location, status)
4. **Refresh:** Updates when `refreshKey` changes or filters are applied
5. **Display:** Renders horizontal bar chart with categories on Y-axis, counts on X-axis

### Filter Integration:

The chart automatically uses these filters from the Overview page:
- Date Range (start_date, end_date)
- Departments
- Locations
- Sublocations
- Statuses
- Violation Types

---

## 📊 Expected Chart Visualization

### Chart Type: Horizontal Bar Chart

```
Top Hazard Findings
─────────────────────────────────────────────────────

No Loss / No Injury                    ████████████████████████████ 292
Site HSE Rules                         ██████████████████████████ 276
Other                                  ███████████ 98
Site HSE Rules; No Loss / No Injury    █████████ 84
Injury                                 ██████ 57
Other; No Loss / No Injury             █████ 55
Equipment Failure                      ██ 18
Property/Asset Damage                  ██ 16
Fire                                   █ 9
Injury; No Loss / No Injury            █ 8
...
```

### Chart Features:
- ✅ Interactive tooltips on hover
- ✅ Shows category name and count
- ✅ Sorted by count (descending)
- ✅ Responsive design
- ✅ Filters apply in real-time

---

## 🔄 Complete Testing Workflow

### Step 1: Start Backend Server

```bash
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\server"
uvicorn app.main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 2: Test API Endpoint

**PowerShell:**
```powershell
# Test endpoint
curl http://localhost:8000/analytics/data/hazard-top-findings

# Or use Invoke-RestMethod for better formatting
$result = Invoke-RestMethod -Uri "http://localhost:8000/analytics/data/hazard-top-findings"
Write-Host "Found $($result.labels.Count) categories"
$result.labels[0..4]  # Show top 5
$result.series[0].data[0..4]  # Show top 5 counts
```

### Step 3: Start Frontend

```bash
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\client"
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 4: View in Browser

1. Open: http://localhost:5173
2. Navigate to Overview page
3. Scroll to "Top Hazard Findings" chart
4. Verify chart shows incident type categories with counts

### Step 5: Test Filters

1. Click "Filters" button
2. Select date range: 2023-03-01 to 2023-12-31
3. Select department: HPO
4. Click outside filter panel
5. Verify chart updates with filtered data

---

## 🐛 Troubleshooting

### Issue 1: Chart Shows "No Data Available"

**Possible Causes:**
1. Backend server not running
2. Excel file not found
3. No 'Incident Type(s)' column in data

**Solutions:**
```bash
# Check server is running
curl http://localhost:8000/health

# Check endpoint directly
curl http://localhost:8000/analytics/data/hazard-top-findings

# Run test script
cd server
python test_hazard_findings.py
```

### Issue 2: Chart Shows Wrong Data

**Possible Causes:**
1. Cache not cleared after Excel update
2. Filters too restrictive

**Solutions:**
```bash
# Restart server to clear cache
# Stop server (Ctrl+C)
# Start server again
uvicorn app.main:app --reload --port 8000

# Clear all filters in UI
# Click "Clear All" button in filter panel
```

### Issue 3: CORS Error in Frontend

**Possible Causes:**
- Backend and frontend running on different ports

**Solutions:**
Check `server/app/main.py` CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📈 Data Quality Tips

### For Best Results:

1. **Consistent Categories**: Ensure incident types are standardized in Excel
2. **No Empty Values**: Fill in "Other" for unknown types instead of leaving blank
3. **Proper Delimiters**: Use semicolons (;) to separate multiple incident types
4. **No Typos**: "No Loss / No Injury" should always have same spelling/spacing

### Cleaning Data in Excel:

```
Bad Examples:
- "no loss/no injury" (wrong spacing)
- "NoLoss/NoInjury" (no spaces)
- "" (empty)
- "N/A" (placeholder)

Good Examples:
- "No Loss / No Injury"
- "Site HSE Rules"
- "Other"
- "Site HSE Rules; No Loss / No Injury"
```

---

## 🎯 Summary

### What Changed:
1. ✅ Backend endpoint now analyzes `Incident Type(s)` column
2. ✅ Returns category counts instead of text descriptions
3. ✅ Shows ALL categories (no 20-item limit)
4. ✅ Better data cleaning and normalization

### What Stayed the Same:
1. ✅ Frontend component (no changes needed)
2. ✅ Filtering system (all filters still work)
3. ✅ API endpoint URL (same path)
4. ✅ Response format (same JSON structure)

### Testing Checklist:
- [x] Backend test script passes
- [x] API endpoint accessible
- [ ] Frontend chart displays correctly
- [ ] Filters work as expected
- [ ] Data matches Excel source

---

## 📝 Next Steps

1. **Start the backend server**:
   ```bash
   cd server
   uvicorn app.main:app --reload --port 8000
   ```

2. **Test the endpoint**:
   ```powershell
   curl http://localhost:8000/analytics/data/hazard-top-findings
   ```

3. **Start the frontend**:
   ```bash
   cd client
   npm run dev
   ```

4. **Verify in browser**: http://localhost:5173

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-14  
**Status:** ✅ Backend Tested & Working | ⏳ Frontend Testing Pending
