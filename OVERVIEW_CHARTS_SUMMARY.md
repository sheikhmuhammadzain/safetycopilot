# Overview Charts - Quick Reference Summary

## Chart Index

| # | Chart Name | Type | Data Source | Key Metric | Filters |
|---|------------|------|-------------|------------|---------|
| 1 | **KPI Cards (6x)** | Count cards | Multiple sheets | Row counts | ✅ All |
| 2 | **Hazards Trend** | Line (daily) | Hazard ID | Count per day | ✅ All + per-chart dates |
| 3 | **Incidents Trend** | Line (daily) | Incident | Count per day | ✅ All + per-chart dates |
| 4 | **Root Cause Pareto** | Bars + Line | Incident | Count + cumulative % | ✅ All + incident type |
| 5 | **Hazards by Type** | Horizontal bars | Hazard ID | Count by category | ✅ All |
| 6 | **Incidents by Severity** | Stacked bars | Hazard ID | Count by type × severity | ✅ All |
| 7 | **Audit Findings** | Horizontal bars | Audit | Top 20 findings | ✅ Most |
| 8 | **Inspection Findings** | Horizontal bars | Inspection | Top 20 findings | ✅ Most |
| 9 | **Dept × Month Heatmap** | Heatmap | Incident | Avg score or count | ✅ All |
| 10 | **Recent Incidents** | List | Incident | Last 5 items | ❌ None |
| 11 | **Recent Hazards** | List | Hazard ID | Last 5 items | ❌ None |
| 12 | **Recent Audits** | List | Audit | Last 5 items | ❌ None |

---

## Quick Formula Reference

> Update (KPI counting): The /data-health/counts/all endpoint returns GLOBAL totals using unique, non-null ID columns and ignores filters. Hazards currently use the "Incident Number" column on the Hazard sheet. Findings KPIs count unique "Audit Number" in sheets selected by name tokens ("audit find", "inspection find").

### KPI Cards
```python
count = len(df)  # After filters
```

### Trend Charts (Hazards/Incidents)
```python
# Daily counts
dates = pd.to_datetime(df['date_col']).dt.date
counts = dates.value_counts().sort_index()
```

### Root Cause Pareto
```python
# Top N root causes
counts = df['root_cause'].value_counts().head(15)
cumulative_pct = (counts.cumsum() / counts.sum()) * 100
```

### Hazards by Type
```python
# All incident type categories
counts = df['incident_type'].value_counts()
# No limit, all returned
```

### Incidents by Severity (Stacked)
```python
# Crosstab: incident_type × severity
matrix = pd.crosstab(df['incident_type'], df['severity'])
# Group types with count < 8 as "Others"
```

### Audit/Inspection Findings
```python
# Top 20 findings (cleaned text)
series = df['finding'].dropna()
series = clean_and_normalize(series)
counts = series.value_counts().head(20)
```

### Department × Month Heatmap
```python
# Pivot table
pivot = df.pivot_table(
    values='risk_score',  # or count
    index='department',
    columns='month',
    aggfunc='mean'  # or 'count'
)
```

### Recent Items
```python
# Sort by date descending
df = df.sort_values('date', ascending=False).head(5)
```

---

## Data Sources Quick Reference

### Excel Sheets Used

| Sheet | Used By | Key Columns |
|-------|---------|-------------|
| **Incident** | KPIs, Incidents Trend, Root Cause Pareto, Dept×Month Heatmap, Recent Incidents | Date of Occurrence, Root Cause, Department, Status, Title |
| **Hazard ID** | KPIs, Hazards Trend, Hazards by Type, Incidents by Severity, Recent Hazards | Date Entered, Incident Type(s), Worst Case Consequence Potential, Status, Title |
| **Audit** | KPIs, Audit Findings, Recent Audits | finding/observation, scheduled_date, audit_status, Title |
| **Inspection** | KPIs, Inspection Findings | finding/observation, start_date, audit_status |

---

## Endpoint Quick Reference

### Data Health (KPIs)
```
GET /data-health/counts/all  # Note: filters are ignored by this endpoint
```

### Trend Charts
```
GET /analytics/data/incident-trend-detailed?dataset={hazard|incident}&[filters]
```

### Root Cause Pareto
```
GET /analytics/data/root-cause-pareto?dataset=incident&incident_type={All|type}&[filters]
GET /analytics/data/root-cause-pareto/incident-types  # For radio options
```

### Hazards by Type
```
GET /analytics/data/hazard-top-findings?dataset=hazard&[filters]
```

### Incidents by Severity
```
GET /analytics/data/incident-top-findings?dataset=incident&min_count=8&[filters]
```

### Audit Findings
```
GET /analytics/data/audit-top-findings?[filters]
```

### Inspection Findings
```
GET /analytics/data/inspection-top-findings?[filters]
```

### Department × Month Heatmap
```
GET /analytics/data/department-month-heatmap?dataset=incident&[filters]
```

### Recent Items
```
GET /data/incidents/recent?limit=5
GET /data/hazards/recent?limit=5
GET /data/audits/recent?limit=5
```

---

## Filter Parameters

### Available Filters

```javascript
{
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: ["Dept1", "Dept2"],
  locations: ["Location1"],
  sublocations: ["Subloc1"],
  statuses: ["Open", "Closed"],
  incident_types: ["Type1"],
  violation_types: ["Violation1"],
  min_severity: 0,
  max_severity: 5,
  min_risk: 0,
  max_risk: 5
}
```

### Which Charts Support Which Filters

| Chart | Date | Dept | Location | Subloc | Status | Types | Severity | Risk |
|-------|------|------|----------|--------|--------|-------|----------|------|
| KPIs | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Trends | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Pareto | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Hazards by Type | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Inc by Severity | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Findings | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Heatmap | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Recent Items | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

---

## Column Name Resolution

The backend uses flexible column name matching. Here are the patterns:

### Date Columns
```python
# Incidents
["occurrence_date", "date of occurrence", "date reported", "date entered"]

# Hazards
["date_entered", "date entered", "date reported", "occurrence_date"]

# Audits
["scheduled_date", "start_date"]
```

### Department Columns
```python
["department", "section"]
```

### Root Cause Columns
```python
["Root Cause", "root_cause", "Key Factor", "key_factor", "Contributing Factor"]
```

### Incident Type Columns
```python
["incident_type(s)", "incident type(s)", "incident_types", "incident type", "incident_type"]
```

### Severity Columns
```python
["severity_score", "severity", "actual consequence (incident)", "worst case consequence potential (hazard id)"]
```

### Risk Columns
```python
["risk_score", "risk"]
```

### Findings Columns
```python
["finding", "findings", "observation", "observations", "non_conformance", "non conformance",
 "issue", "issues", "remark", "remarks", "description", "checklist_category"]
```

---

## Color Schemes

### Severity Colors (Stacked Bar)
```javascript
{
  "C0 - No Ill Effect": "#10b981",  // Green
  "C1 - Minor": "#fbbf24",          // Yellow
  "C2 - Serious": "#f97316",        // Orange
  "C3 - Severe": "#ef4444"          // Red
}
```

### KPI Card Icons
```javascript
{
  Incidents: "AlertTriangle" (amber),
  Hazards: "ShieldAlert" (rose),
  Audits: "FileCheck" (accent),
  Inspections: "ClipboardCheck" (emerald),
  Findings: "ListChecks" (amber)
}
```

### Chart Colors
- **Primary**: Line charts, bar charts
- **Secondary**: Trend lines, secondary series
- **Heatmap**: Yellow-Orange-Red gradient (d3.interpolateYlOrRd)

---

## Performance Benchmarks

| Operation | Typical Time |
|-----------|--------------|
| Load Excel data (cached) | < 1s |
| Apply filters | < 50ms |
| Calculate KPIs | < 100ms |
| Generate trend data | < 200ms |
| Build Pareto chart | < 300ms |
| Create heatmap | < 500ms |
| Fetch recent items | < 100ms |

**Total Page Load**: ~2-3 seconds (including all 12 charts)

---

## Data Cleaning Patterns

### Common Cleaning Steps

1. **Normalize whitespace**: `str.replace(r"\s+", " ", regex=True)`
2. **Strip punctuation**: `str.strip(" \t\r\n-–•·;:,.")`
3. **Remove non-breaking spaces**: `str.replace("\xa0", " ")`
4. **Replace null placeholders**: `replace({"nan": pd.NA, "None": pd.NA})`
5. **Drop NA values**: `dropna()`

### Excluded Patterns

```python
# NA patterns
r"^(n/?a|na|nan|null|none|not\s*applicable)$"

# "No" patterns (for findings)
r"^no(\s+|$)|no\s+(finding|observation|issue)$"
```

---

## Frontend Components Used

| Chart | Component | Library |
|-------|-----------|---------|
| KPI Cards | `KPICard` | Custom |
| Trend Charts | `ShadcnLineCardEnhanced` | Recharts + Shadcn |
| Pareto | `ShadcnParetoCard` | Recharts + Shadcn |
| Bar Charts | `ShadcnBarCard` | Recharts + Shadcn |
| Stacked Bar | `StackedBarCard` | Recharts |
| Heatmap | `ShadcnHeatmapCard` | Custom (D3) |
| Recent Lists | `RecentList` | Custom |

---

## Architecture Summary

```
Excel Files (EPCL_VEHS_Data_Processed.xlsx)
    ↓
Backend (FastAPI + Pandas)
    ↓ (LRU Cache)
Data Processing & Aggregation
    ↓ (Filters Applied)
JSON Response
    ↓
Frontend (React + React Query)
    ↓ (State Management)
Chart Components (Recharts/D3)
    ↓
User Interface
```

---

## Testing Checklist

When testing charts, verify:

- [ ] Data loads correctly from Excel
- [ ] Filters apply and update charts
- [ ] Date ranges work (global + per-chart)
- [ ] Column names resolve flexibly
- [ ] Charts render without errors
- [ ] Tooltips show correct data
- [ ] Colors match specifications
- [ ] Performance is acceptable (< 500ms per chart)
- [ ] Empty states handled gracefully
- [ ] Recent items sorted by date (newest first)

---

## Common Issues & Solutions

### Issue: Chart shows no data
**Solution**: Check if date column exists and has valid dates

### Issue: Wrong column used
**Solution**: Verify column name resolution order in backend

### Issue: Filters not applying
**Solution**: Check filter parameters are being passed correctly

### Issue: Slow performance
**Solution**: Check Excel file size and filter complexity

### Issue: Recent items in wrong order
**Solution**: Verify date column sorting (descending)

---

## Related Documentation

- **Full Report**: `OVERVIEW_CHARTS_REPORT.md` - Detailed documentation
- **Recent Items Guide**: `RECENT_ITEMS_GUIDE.md` - Recent items endpoints
- **Filter Integration**: See filter_options.py and filters.py
- **Backend Endpoints**: server/app/routers/analytics_general.py
- **Frontend**: client/src/pages/Overview.tsx

---

**Last Updated**: 2025-10-14  
**Version**: 1.0  
**Total Charts**: 12 (6 KPIs + 6 visualizations)
