# 🚀 Quick Start Guide - Testing Updated Hazard Findings

## ✅ What Was Changed

**Backend:**
- `server/app/routers/analytics_general.py` - Updated `/data/hazard-top-findings` endpoint
- Now shows **Incident Type Categories** (e.g., "No Loss / No Injury", "Site HSE Rules") instead of text descriptions

**Frontend:**
- `client/src/pages/Overview.tsx` - Updated chart title and tooltip
- Changed from "Top Hazard Findings" to "Hazards by Incident Type Category"

## 🧪 Testing Steps

### Step 1: Start Backend Server

```powershell
# Navigate to server directory
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\server"

# Start server
uvicorn app.main:app --reload --port 8000
```

**Wait for:** `Application startup complete.`

---

### Step 2: Test Backend Endpoint

**Open a NEW PowerShell window** and run:

```powershell
# Test the endpoint
$response = Invoke-RestMethod -Uri "http://localhost:8000/analytics/data/hazard-top-findings"

# Display results
Write-Host "`n✅ SUCCESS! Found $($response.labels.Count) incident type categories`n" -ForegroundColor Green

Write-Host "Top 10 Categories:" -ForegroundColor Cyan
for ($i = 0; $i -lt [Math]::Min(10, $response.labels.Count); $i++) {
    $label = $response.labels[$i]
    $count = $response.series[0].data[$i]
    Write-Host "  $($i+1). $label - $count hazards"
}

Write-Host "`nTotal hazards: $(($response.series[0].data | Measure-Object -Sum).Sum)" -ForegroundColor Yellow
```

**Expected Output:**
```
✅ SUCCESS! Found 50 incident type categories

Top 10 Categories:
  1. No Loss / No Injury - 292 hazards
  2. Site HSE Rules - 276 hazards
  3. Other - 98 hazards
  4. Site HSE Rules; No Loss / No Injury - 84 hazards
  5. Injury - 57 hazards
  6. Other; No Loss / No Injury - 55 hazards
  7. Equipment Failure - 18 hazards
  8. Property/Asset Damage - 16 hazards
  9. Fire - 9 hazards
  10. Injury; No Loss / No Injury - 8 hazards

Total hazards: 994
```

---

### Step 3: Test with Filters

```powershell
# Test with date filter
$params = @{
    start_date = "2023-03-01"
    end_date = "2023-12-31"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/analytics/data/hazard-top-findings" -Body $params

Write-Host "`n✅ With date filter: Found $($response.labels.Count) categories" -ForegroundColor Green
Write-Host "Total hazards: $(($response.series[0].data | Measure-Object -Sum).Sum)"
```

---

### Step 4: Start Frontend

**Open a NEW PowerShell window** (keep backend running):

```powershell
# Navigate to client directory
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\client"

# Start frontend
npm run dev
```

**Wait for:** `Local:   http://localhost:5173/`

---

### Step 5: View in Browser

1. Open browser to: **http://localhost:5173**
2. Navigate to **Overview** page (should be default)
3. Scroll down to find: **"Hazards by Incident Type Category"** chart
4. Verify chart shows:
   - Horizontal bars
   - Category names on Y-axis (e.g., "No Loss / No Injury")
   - Counts on X-axis
   - Sorted by count (highest first)

---

### Step 6: Test Filters in UI

1. Click **"Filters"** button at top of page
2. Apply filters:
   - Date Range: **2023-03-01** to **2023-12-31**
   - Department: Select **HPO** or **PVC**
3. Click outside the filter panel
4. Verify chart updates automatically

---

## 📊 Expected Chart Appearance

```
Hazards by Incident Type Category
─────────────────────────────────────────────────

No Loss / No Injury           ███████████████ 292
Site HSE Rules                ██████████████ 276
Other                         █████ 98
Site HSE Rules; No Loss...   ████ 84
Injury                        ██ 57
Other; No Loss / No Injury   ██ 55
Equipment Failure            █ 18
Property/Asset Damage        █ 16
Fire                         █ 9
...
```

---

## ✅ Verification Checklist

- [ ] Backend server starts without errors
- [ ] Endpoint returns 50 categories
- [ ] Top category is "No Loss / No Injury" (292 hazards)
- [ ] Total hazards = 994
- [ ] Frontend starts successfully
- [ ] Chart displays on Overview page
- [ ] Chart title: "Hazards by Incident Type Category"
- [ ] Bars show categories on Y-axis, counts on X-axis
- [ ] Tooltip shows updated information
- [ ] Filters work and update chart
- [ ] Data matches backend response

---

## 🐛 Troubleshooting

### Backend server won't start
```powershell
# Check if port 8000 is already in use
netstat -ano | findstr :8000

# If occupied, kill the process or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend can't connect to backend
```powershell
# Verify backend is running
curl http://localhost:8000/health

# Check CORS configuration in server/app/main.py
# Should include: allow_origins=["http://localhost:5173"]
```

### Chart shows "No data available"
```powershell
# Test endpoint directly
curl http://localhost:8000/analytics/data/hazard-top-findings

# If empty response, check Excel file exists:
Test-Path "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\server\app\EPCL_VEHS_Data_Processed.xlsx"
```

### Chart shows old data
```powershell
# Clear cache by restarting backend server
# Press Ctrl+C to stop
# Run uvicorn command again
```

---

## 📝 Quick Commands Summary

```powershell
# Terminal 1: Backend
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\server"
uvicorn app.main:app --reload --port 8000

# Terminal 2: Test Endpoint
Invoke-RestMethod -Uri "http://localhost:8000/analytics/data/hazard-top-findings"

# Terminal 3: Frontend  
cd "C:\Users\ibrahim laptops\Desktop\qbit\safteycopilot\client"
npm run dev

# Browser: http://localhost:5173
```

---

## 🎯 Success Criteria

✅ You're done when:
1. Backend returns 50 incident type categories
2. Frontend chart displays with new title
3. Categories like "No Loss / No Injury", "Site HSE Rules" are visible
4. Counts match backend (292, 276, 98, etc.)
5. Filters update the chart in real-time

---

**Happy Testing! 🎉**

Need help? Check:
- `HAZARD_FINDINGS_INTEGRATION_GUIDE.md` for detailed documentation
- `HAZARD_TOP_FINDINGS_ANALYSIS.md` for technical deep dive
