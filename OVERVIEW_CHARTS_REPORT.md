# Safety Copilot - Overview Section Charts Report

## Executive Summary

This document provides a comprehensive analysis of all charts displayed in the Overview section of the Safety Copilot dashboard. For each chart, we document:

- **Data source** (Excel sheet and columns)
- **Backend endpoint** processing the data
- **Calculation formulas** and aggregations
- **Filter parameters** that can be applied
- **Visualization type** and purpose

---

## Table of Contents

1. [KPI Cards](#1-kpi-cards)
2. [Hazards Trend (Line Chart)](#2-hazards-trend-line-chart)
3. [Incidents Trend (Line Chart)](#3-incidents-trend-line-chart)
4. [Root Cause Pareto Chart](#4-root-cause-pareto-chart)
5. [Hazards by Incident Type Category (Bar Chart)](#5-hazards-by-incident-type-category-bar-chart)
6. [Incidents by Type and Severity (Stacked Bar Chart)](#6-incidents-by-type-and-severity-stacked-bar-chart)
7. [Top Audit Findings (Bar Chart)](#7-top-audit-findings-bar-chart)
8. [Top Inspection Findings (Bar Chart)](#8-top-inspection-findings-bar-chart)
9. [Department × Month Heatmap](#9-department--month-heatmap)
10. [Recent Items Lists](#10-recent-items-lists)

---

## 1. KPI Cards

### 1.1 Incidents KPI Card

**Purpose**: Display total count of incidents

**Data Source**:

- **Sheet**: `Incident`
- **Columns Used**: `Incident Number` (unique, non-null)

**Backend Endpoint**: `/data-health/counts/all`

**Formula**:

```python
# Counts unique, non-null IDs (no filters applied)
count = incident_df["Incident Number"].dropna().nunique()
```

**Important behavior**:

- The endpoint does NOT apply any filters. Totals are global across the entire sheet.

**Calculation Logic**:

1. Load Incident DataFrame
2. Count unique, non-null values in `Incident Number`
3. Return the count

**Filter Support**:

- ❌ None (endpoint currently ignores any filter parameters)

**Frontend Component**: `KPICard`

- Icon: `AlertTriangle`
- Variant: `warning` (amber)

---

### 1.2 Hazards KPI Card

**Purpose**: Display total count of hazards

**Data Source**:

- **Sheet**: `Hazard ID`
- **Columns Used**: `Incident Number` (unique, non-null) — Note: current implementation uses this column in the Hazard sheet.

**Backend Endpoint**: `/data-health/counts/all`

**Formula**:

```python
# Counts unique, non-null IDs from the Hazard sheet
# (current code uses "Incident Number" as the ID column)
count = hazard_df["Incident Number"].dropna().nunique()
```

**Important behavior**:

- No filters are applied.
- If your Hazard sheet has a dedicated `Hazard ID`/`Hazard Number`, the backend can be updated to use it. Current behavior counts unique `Incident Number` values.

**Filter Support**: ❌ None (endpoint ignores filters)

**Frontend Component**: `KPICard`

- Icon: `ShieldAlert`
- Variant: `danger` (rose)

---

### 1.3 Audits KPI Card

**Purpose**: Display total count of audits

**Data Source**:

- **Sheet**: `Audit`
- **Columns Used**: `Audit Number` (unique, non-null)

**Backend Endpoint**: `/data-health/counts/all`

**Formula**:

```python
count = audit_df["Audit Number"].dropna().nunique()
```

**Filter Support**: ❌ None (endpoint ignores filters)

**Frontend Component**: `KPICard`

- Icon: `FileCheck`
- Variant: `default` (accent)

---

### 1.4 Inspections KPI Card

**Purpose**: Display total count of inspections

**Data Source**:

- **Sheet**: `Inspection`
- **Columns Used**: `Audit Number` (unique, non-null)

**Backend Endpoint**: `/data-health/counts/all`

**Formula**:

```python
count = inspection_df["Audit Number"].dropna().nunique()
```

**Filter Support**: ❌ None (endpoint ignores filters)

**Frontend Component**: `KPICard`

- Icon: `ClipboardCheck`
- Variant: `success` (emerald)

---

### 1.5 Audit Findings KPI Card

**Purpose**: Display total count of audits-with-findings (not raw finding rows)

**Backend Endpoint**: `/data-health/counts/all`

**How it counts**:

- The backend selects a sheet whose name contains both tokens: "audit" and "find" (prefers exact/stronger matches).
- It then counts unique, non-null `Audit Number` values in that sheet.
- This represents the number of distinct audits that have findings, not the total number of findings records.

**Filter Support**: ❌ None (endpoint ignores filters)

**Frontend Component**: `KPICard`

- Icon: `ListChecks`
- Variant: `warning` (amber)

---

### 1.6 Inspection Findings KPI Card

**Purpose**: Display total count of inspections-with-findings (not raw finding rows)

**Backend Endpoint**: `/data-health/counts/all`

**How it counts**:

- The backend selects a sheet whose name contains both tokens: "inspection" and "find".
- It counts unique, non-null `Audit Number` values in that sheet.
- This approximates the number of distinct inspections that have findings.

**Filter Support**: ❌ None (endpoint ignores filters)

**Frontend Component**: `KPICard`

- Icon: `ListChecks`
- Variant: `warning` (amber)

---

## 2. Hazards Trend (Line Chart)

### Overview

**Component**: `ShadcnLineCardEnhanced`  
**Title**: "Hazards Trend"  
**Purpose**: Shows the number of hazards identified each day over time

### Data Source

**Sheet**: `Hazard ID`

**Columns Used**:

- `Date Entered` (primary) OR `Date Reported` OR `occurrence_date` (fallbacks)
- All hazard rows

**Backend Endpoint**: `/analytics/data/incident-trend-detailed`

**Query Parameters**:

```javascript
{
  dataset: "hazard",
  start_date: "YYYY-MM-DD", // From per-chart filter
  end_date: "YYYY-MM-DD",   // From per-chart filter
  departments: ["Dept1", "Dept2"],
  locations: [...],
  sublocations: [...],
  statuses: [...],
  violation_types: [...]
}
```

### Calculation Formula

```python
def calculate_hazards_trend(hazard_df, filters):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(hazard_df, **filters)

    # 2. Find date column (in order of preference)
    date_col = resolve_column(filtered_df, [
        "date_entered",
        "date reported",
        "occurrence_date"
    ])

    # 3. Convert to daily periods (YYYY-MM-DD format)
    dates = pd.to_datetime(filtered_df[date_col], errors='coerce')
    daily_dates = dates.dt.date.astype(str)

    # 4. Count hazards per day
    counts = daily_dates.value_counts().sort_index()

    # 5. Return as time series
    return {
        "labels": counts.index.tolist(),  # Dates (x-axis)
        "series": [{
            "name": "Count",
            "data": counts.values.astype(int).tolist()  # Counts (y-axis)
        }]
    }
```

### Enhanced Details (Tooltips)

The endpoint also returns detailed breakdown for each day:

```python
details_per_day = {
    "month": "2023-05-20",
    "total_count": 15,
    "departments": [
        {"name": "Process - EDC / VCM", "count": 8},
        {"name": "PVC", "count": 5}
    ],
    "types": [  # Violation types
        {"name": "Unsafe Act", "count": 10},
        {"name": "Safety Rule Violation", "count": 5}
    ],
    "severity": {
        "avg": 2.5,
        "max": 4.0,
        "min": 1.0
    },
    "risk": {
        "avg": 3.2,
        "max": 5.0,
        "min": 2.0
    },
    "recent_items": [
        {
            "title": "Hazard description...",
            "department": "Production",
            "date": "2023-05-20",
            "severity": 3.0
        }
    ]
}
```

### Granularity

- **Daily** (YYYY-MM-DD)
- Allows per-chart date range filtering independent of global filters

### Filter Support

✅ **All filters apply:**

- Per-chart date range (overrides global dates)
- Global departments
- Global locations
- Global sublocations
- Global statuses
- Global violation types

### Visualization

- **Type**: Area line chart (smoothed curve)
- **X-axis**: Dates (chronological)
- **Y-axis**: Count of hazards
- **Color**: Primary theme color with gradient fill
- **Interactivity**: Hover tooltips show detailed breakdown

---

## 3. Incidents Trend (Line Chart)

### Overview

**Component**: `ShadcnLineCardEnhanced`  
**Title**: "Incidents Trend"  
**Purpose**: Displays the total number of incidents reported each day

### Data Source

**Sheet**: `Incident`

**Columns Used**:

- `Date of Occurrence` (primary) OR `Date Reported` OR `Date Entered` (fallbacks)
- All incident rows

**Backend Endpoint**: `/analytics/data/incident-trend-detailed`

**Query Parameters**: Same structure as Hazards Trend but with `dataset: "incident"`

### Calculation Formula

```python
def calculate_incidents_trend(incident_df, filters):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(incident_df, **filters)

    # 2. Find date column (preference order)
    date_col = resolve_column(filtered_df, [
        "occurrence_date",
        "date of occurrence",
        "date reported",
        "date entered"
    ])

    # 3. Convert to daily periods
    dates = pd.to_datetime(filtered_df[date_col], errors='coerce')
    daily_dates = dates.dt.date.astype(str)

    # 4. Count incidents per day
    counts = daily_dates.value_counts().sort_index()

    return {
        "labels": counts.index.tolist(),
        "series": [{
            "name": "Count",
            "data": counts.values.astype(int).tolist()
        }]
    }
```

### Enhanced Details

Similar to Hazards Trend, includes per-day breakdown:

- Top departments with counts
- Top incident types with counts
- Severity statistics (avg, max, min)
- Risk statistics
- Recent incidents (up to 5)

### Example Response

```json
{
  "labels": ["2023-01-01", "2023-01-02", "2023-01-03"],
  "series": [{
    "name": "Count",
    "data": [5, 8, 3]
  }],
  "details": [
    {
      "month": "2023-01-01",
      "total_count": 5,
      "departments": [
        {"name": "Production", "count": 3},
        {"name": "Maintenance", "count": 2}
      ],
      "types": [
        {"name": "Equipment Failure", "count": 3},
        {"name": "Human Error", "count": 2}
      ],
      "severity": {"avg": 2.4, "max": 4.0, "min": 1.0},
      "recent_items": [...]
    }
  ]
}
```

### Filter Support

✅ **All filters apply** (same as Hazards Trend)

### Visualization

- **Type**: Area line chart
- **X-axis**: Dates
- **Y-axis**: Count of incidents
- **Color**: Secondary theme color with gradient

---

## 4. Root Cause Pareto Chart

### Overview

**Component**: `ShadcnParetoCard`  
**Title**: "Root Cause Pareto"  
**Purpose**: Identifies the top root causes responsible for most incidents (80/20 rule)

### Data Source

**Sheet**: `Incident`

**Columns Used**:

- `Root Cause` (primary) OR `Key Factor` OR `Contributing Factor` (fallbacks)
- `Incident Type(s)` (for optional filtering by incident type)

**Backend Endpoint**: `/analytics/data/root-cause-pareto`

**Query Parameters**:

```javascript
{
  dataset: "incident",
  incident_type: "All" | "specific_type",  // Radio button selection
  top_n: 15,  // Number of top causes to show
  // Plus all global filters
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: [...],
  locations: [...],
  sublocations: [...],
  statuses: [...],
  incident_types: [...]
}
```

### Calculation Formula

```python
def calculate_root_cause_pareto(incident_df, filters, incident_type, top_n=15):
    # 1. Apply standard filters
    filtered_df = apply_analytics_filters(incident_df, **filters)

    # 2. Optional: Filter by specific incident type (from radio button)
    if incident_type and incident_type != "All":
        type_col = resolve_column(filtered_df, ["incident_type(s)"])
        # Split multi-value types (separated by semicolons)
        filtered_df["_type_split"] = filtered_df[type_col].str.split(";")
        filtered_df = filtered_df.explode("_type_split")
        filtered_df["_type_split"] = filtered_df["_type_split"].str.strip()
        # Case-insensitive match
        filtered_df = filtered_df[
            filtered_df["_type_split"].str.lower() == incident_type.lower()
        ]

    # 3. Extract root causes
    rc_col = resolve_column(filtered_df, [
        "Root Cause",
        "root_cause",
        "Key Factor",
        "Contributing Factor"
    ])

    # 4. Split on semicolons and explode (handle multi-value root causes)
    root_causes = filtered_df[rc_col].dropna().astype(str)
    root_causes = root_causes.str.split(";").explode().str.strip()

    # 5. Remove empty and placeholder values
    root_causes = root_causes[root_causes != ""]
    root_causes = root_causes[
        ~root_causes.str.contains("nan|null|none|n/a", case=False, regex=True)
    ]

    # 6. Count and get top N
    counts = root_causes.value_counts().head(top_n)

    # 7. Calculate cumulative percentage for Pareto line
    total = counts.sum()
    cumulative_pct = (counts.cumsum() / total * 100).round(2)

    return {
        "labels": counts.index.tolist(),      # Root cause names (x-axis)
        "bars": counts.values.tolist(),       # Counts (left y-axis, bars)
        "cum_pct": cumulative_pct.tolist(),  # Cumulative % (right y-axis, line)
        "incident_type": incident_type,
        "total_count": int(counts.sum())
    }
```

### Pareto Formula

**Cumulative Percentage**:

```
For cause i at position n:
  cumulative_pct[n] = (Σ(counts[0...n]) / Σ(total_counts)) × 100
```

**80/20 Rule Application**:

- Chart shows which root causes contribute to 80% of all incidents
- Line crosses 80% threshold typically at top 3-5 causes
- Helps prioritize corrective actions

### Example Response

```json
{
  "labels": [
    "Inadequate preventive maintenance",
    "Incomplete planning process",
    "Worker fatigue/distraction",
    "Communication gaps",
    "Equipment malfunction"
  ],
  "bars": [120, 95, 78, 65, 42],
  "cum_pct": [30.0, 53.75, 73.25, 89.5, 100.0],
  "incident_type": "All",
  "total_count": 400
}
```

### Incident Type Filter

**Additional Endpoint**: `/analytics/data/root-cause-pareto/incident-types`

Returns available incident types as radio button options:

```json
{
  "incident_types": [
    {"label": "All", "value": "All", "count": 866},
    {"label": "Site HSE Rules", "value": "Site HSE Rules", "count": 276},
    {"label": "Other", "value": "Other", "count": 195},
    {
      "label": "No Loss / No Injury",
      "value": "No Loss / No Injury",
      "count": 292
    }
  ]
}
```

### Filter Support

✅ **All filters apply** + incident type radio filter

### Visualization

- **Type**: Combination chart (bars + line)
- **Bars**: Count of incidents per root cause (left y-axis)
- **Line**: Cumulative percentage (right y-axis, 0-100%)
- **80% Line**: Horizontal reference line at 80%
- **Colors**: Bars (blue), Line (red), 80% line (dashed gray)

---

## 5. Hazards by Incident Type Category (Bar Chart)

### Overview

**Component**: `ShadcnBarCard`  
**Title**: "Hazards by Incident Type Category"  
**Purpose**: Breakdown of hazards grouped by incident type categories

### Data Source

**Sheet**: `Hazard ID`

**Columns Used**:

- `Incident Type(s)` - Categories like:
  - "No Loss / No Injury"
  - "Site HSE Rules"
  - "Injury"
  - "Property/Asset Damage"
  - "Transport Safety"
  - "Other"
  - Combined categories (e.g., "Injury; Site HSE Rules")

**Backend Endpoint**: `/analytics/data/hazard-top-findings`

**Query Parameters**:

```javascript
{
  dataset: "hazard",
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: [...],
  locations: [...],
  sublocations: [...],
  statuses: [...],
  violation_types: [...]
}
```

### Calculation Formula

```python
def calculate_hazards_by_incident_type(hazard_df, filters):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(hazard_df, **filters)

    # 2. Find Incident Type column
    col = resolve_column(filtered_df, [
        "incident_type(s)",
        "incident type(s)",
        "incident_types",
        "incident type"
    ])

    # 3. Clean the column
    series = (
        filtered_df[col]
        .astype(str)
        .str.replace("\xa0", " ", regex=False)  # Remove non-breaking spaces
        .str.replace(r"\s+", " ", regex=True)   # Normalize whitespace
        .str.strip()
        .replace({
            "": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
            "None": pd.NA,
            "null": pd.NA
        })
        .dropna()
    )

    # 4. Count occurrences of each category
    # Note: Combined categories (e.g., "Injury; Site HSE Rules")
    # are treated as single unique categories
    counts = series.value_counts().sort_values(ascending=False)

    # 5. Return ALL categories (no limit)
    return {
        "labels": counts.index.tolist(),        # Category names
        "series": [{
            "name": "Hazards",
            "data": counts.values.tolist()      # Counts per category
        }]
    }
```

### Data Cleaning Steps

1. **Remove non-breaking spaces** (`\xa0`)
2. **Normalize whitespace** (multiple spaces → single space)
3. **Trim leading/trailing spaces**
4. **Replace null placeholders** (nan, NaN, None, null, empty string)
5. **Drop NA values**

### Example Response

```json
{
  "labels": [
    "No Loss / No Injury",
    "Site HSE Rules",
    "Injury",
    "Property/Asset Damage",
    "Other",
    "Transport Safety",
    "Injury; Site HSE Rules",
    "Fire"
  ],
  "series": [
    {
      "name": "Hazards",
      "data": [292, 276, 85, 62, 45, 28, 15, 8]
    }
  ]
}
```

### Key Characteristics

- **No Limit**: Returns ALL unique incident type categories (not limited to top 20)
- **Combined Categories**: Treats multi-value categories (separated by semicolons) as single unique entries
- **Sorted**: Descending by count (most frequent first)

### Filter Support

✅ **All filters apply**:

- Date range
- Departments
- Locations
- Sublocations
- Statuses
- Violation types

### Visualization

- **Type**: Horizontal bar chart
- **X-axis**: Count of hazards
- **Y-axis**: Incident type categories
- **Color**: Primary theme color
- **Bars**: Sorted by count (highest at top)

---

## 6. Incidents by Type and Severity (from Hazard ID data; Stacked Bar Chart)

### Overview

**Component**: `StackedBarCard`  
**Title**: "Incidents by Type and Severity"  
**Purpose**: Shows hazard records grouped by Incident Type with hazard potential severity distribution (C0–C3)

### Data Source

**Sheet**: `Hazard ID` (IMPORTANT: This chart uses Hazard data; the UI label says "Incidents" because it groups by Incident Type categories.)

**Columns Used**:

- `Incident Type(s)` - Incident categories
- `Worst Case Consequence Potential (Hazard ID)` - Severity levels:
  - C0 - No Ill Effect
  - C1 - Minor
  - C2 - Serious
  - C3 - Severe

**Backend Endpoint**: `/analytics/data/incident-top-findings`

**Query Parameters**:

```javascript
{
  // Note: The backend always uses the Hazard ID sheet (hazard_df);
  // any `dataset` param from the UI is ignored by this endpoint.
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: [...],
  locations: [...],
  sublocations: [...],
  statuses: [...],
  violation_types: [...],
  min_count: 8  // Minimum count to avoid "Others" grouping
}
```

**Backend nuances**:

- Always reads from Hazard ID sheet (hazard_df); it does not switch to Incident sheet.
- Severity uses "Worst Case Consequence Potential (Hazard ID)" and is restricted to C0–C3.
- Low-frequency incident types (count < min_count) are grouped under "Others".

### Calculation Formula

```python
def calculate_incidents_by_type_severity(hazard_df, filters, min_count=8):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(hazard_df, **filters)

    # 2. Find columns
    incident_col = resolve_column(filtered_df, [
        "incident_type(s)",
        "incident type(s)"
    ])

    severity_col = resolve_column(filtered_df, [
        "worst case consequence potential (hazard id)",
        "worst_case_consequence_potential_hazard_id"
    ])

    # 3. Clean both columns
    filtered_df[incident_col] = clean_column(filtered_df[incident_col])
    filtered_df[severity_col] = clean_column(filtered_df[severity_col])

    # 4. Drop rows with NA in either column
    df_clean = filtered_df.dropna(subset=[incident_col, severity_col])

    # 5. Group small incident types into "Others"
    counts = df_clean[incident_col].value_counts()
    main_incidents = counts[counts >= min_count].index

    df_filtered = df_clean[df_clean[incident_col].isin(main_incidents)].copy()

    # Add "Others" group for incident types below min_count
    if (counts < min_count).any():
        others_df = df_clean[~df_clean[incident_col].isin(main_incidents)].copy()
        if not others_df.empty:
            others_df[incident_col] = "Others"
            df_filtered = pd.concat([df_filtered, others_df])

    # 6. Define severity order (C0-C3 only for Hazard ID)
    severity_order = [
        "C0 - No Ill Effect",
        "C1 - Minor",
        "C2 - Serious",
        "C3 - Severe"
    ]

    # 7. Create crosstab (incident type × severity)
    matrix = pd.crosstab(
        df_filtered[incident_col],
        df_filtered[severity_col]
    )

    # 8. Ensure all severity levels exist (add missing with 0)
    for sev in severity_order:
        if sev not in matrix.columns:
            matrix[sev] = 0

    # 9. Order columns and sort rows by total
    matrix = matrix[severity_order]
    matrix["Total"] = matrix.sum(axis=1)
    matrix = matrix.sort_values("Total", ascending=False)
    totals = matrix["Total"].astype(int).tolist()
    matrix = matrix.drop(columns="Total")

    # 10. Build stacked series
    labels = matrix.index.tolist()  # Incident types (x-axis)
    series = [
        {
            "name": sev,
            "data": matrix[sev].astype(int).tolist()
        }
        for sev in severity_order
    ]

    return {
        "labels": labels,
        "series": series,
        "totals": totals,
        "legend": severity_order,
        "records_used": int(df_clean.shape[0]),
        "min_count_for_others": int(min_count)
    }
```

### Example Response

```json
{
  "labels": [
    "Site HSE Rules",
    "No Loss / No Injury",
    "Property/Asset Damage",
    "Others"
  ],
  "series": [
    {
      "name": "C0 - No Ill Effect",
      "data": [180, 250, 40, 25]
    },
    {
      "name": "C1 - Minor",
      "data": [60, 30, 15, 10]
    },
    {
      "name": "C2 - Serious",
      "data": [25, 8, 5, 3]
    },
    {
      "name": "C3 - Severe",
      "data": [11, 4, 2, 2]
    }
  ],
  "totals": [276, 292, 62, 40],
  "legend": ["C0 - No Ill Effect", "C1 - Minor", "C2 - Serious", "C3 - Severe"],
  "records_used": 670,
  "min_count_for_others": 8
}
```

### Severity Color Mapping

```javascript
const severityColors = {
  "C0 - No Ill Effect": "#10b981", // Green
  "C1 - Minor": "#fbbf24", // Yellow
  "C2 - Serious": "#f97316", // Orange
  "C3 - Severe": "#ef4444", // Red
}
```

### "Others" Grouping Logic

```python
# Incident types with count < min_count (default 8) are grouped as "Others"
if incident_count < min_count:
    incident_type = "Others"
```

### Filter Support

✅ **All filters apply** + min_count parameter

### Visualization

- **Type**: Stacked bar chart (Recharts BarChart)
- **X-axis**: Incident type categories
- **Y-axis**: Count of incidents
- **Stacking**: Each bar shows severity breakdown (C0 bottom → C3 top)
- **Colors**: Green (C0) → Red (C3)
- **Height**: 500px
- **Legend**: Shows all severity levels
- **Tooltip**: Shows breakdown per severity level

---

## 7. Top Audit Findings (Bar Chart)

### Overview

**Component**: `ShadcnBarCard`  
**Title**: "Top Audit Findings"  
**Purpose**: Shows the most frequently identified findings from safety audits

### Data Source

**Sheet**: `Audit`

**Columns Used** (in order of preference):

1. `finding` OR `findings`
2. `observation` OR `observations`
3. `non_conformance` OR `non conformance`
4. `issue` OR `issues`
5. `remark` OR `remarks`
6. `description`
7. `checklist_category` OR `checklist category` (fallback)

**Backend Endpoint**: `/analytics/data/audit-top-findings`

**Query Parameters**:

```javascript
{
  dataset: "audit",
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: [...],
  locations: [...],
  sublocations: [...],
  statuses: [...]
}
```

### Calculation Formula

```python
def calculate_audit_top_findings(audit_df, filters):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(audit_df, **filters)

    # 2. Find findings column (prefer granular text over categories)
    col = resolve_column(filtered_df, [
        "finding", "findings",
        "observation", "observations",
        "non_conformance", "non conformance",
        "issue", "issues",
        "remark", "remarks",
        "description",
        "checklist_category", "checklist category"
    ])

    series = filtered_df[col].dropna().astype(str)

    # 3. Normalize whitespace and strip punctuation
    series = series.str.replace(r"\s+", " ", regex=True)
    series = series.str.strip(" \t\r\n-–•·;:,.")

    # 4. Remove placeholders
    na_pattern = r"^(n/?a|na|nan|null|none|not\s*applicable)$"
    no_pattern = r"^no(\s+|$)|no\s+(finding|findings|observation|issue|recommendation)$"

    series = series[~series.str.match(na_pattern, case=False)]
    series = series[~series.str.match(no_pattern, case=False)]
    series = series[series.str.len() > 0]

    # 5. If using category column, split on delimiters
    is_category = col.lower() in ["checklist_category", "checklist category"]
    if is_category:
        series = series.str.split(r"[;,]").explode()
        series = series.str.replace(r"\s+", " ", regex=True).str.strip()
        series = series[series.str.len() > 0]

    # 6. Canonicalize and count
    tokens = series.str.strip().str.replace(r"\s+", " ", regex=True)
    value_counts = tokens.value_counts().head(20)  # Top 20

    return {
        "labels": value_counts.index.tolist(),
        "series": [{
            "name": "Count",
            "data": value_counts.values.tolist()
        }]
    }
```

### Data Cleaning Steps

1. **Whitespace normalization** (multiple spaces → single space)
2. **Strip punctuation** (hyphens, bullets, colons, commas, periods)
3. **Remove placeholder text**:
   - N/A, na, nan, null, none, "not applicable"
   - "No finding", "No findings", "No observation", etc.
4. **Split category values** (if using checklist_category)
5. **Deduplicate** (case-sensitive aggregation after normalization)
6. **Limit to top 20**

### Excluded Patterns (Regex)

```python
# NA patterns
r"^(n/?a|na|nan|null|none|not\s*applicable)$"

# "No" patterns
r"^no(\s+|$)|no\s+(finding|findings|observation|observations|deficien(?:cy|cies)|issue|issues|recommendation(?:s)?)$"
```

### Example Response

```json
{
  "labels": [
    "Incomplete documentation",
    "PPE not worn properly",
    "Housekeeping issues",
    "Equipment not maintained",
    "Emergency exits blocked",
    "Fire extinguisher expired",
    "Safety signs missing",
    "Improper waste disposal"
  ],
  "series": [
    {
      "name": "Count",
      "data": [45, 38, 32, 28, 22, 18, 15, 12]
    }
  ]
}
```

### Filter Support

✅ **Filters apply**:

- Date range
- Departments
- Locations
- Sublocations
- Statuses

### Visualization

- **Type**: Horizontal bar chart
- **X-axis**: Count
- **Y-axis**: Finding descriptions
- **Limit**: Top 20 findings
- **Color**: Primary theme color
- **Sort**: Descending by count

---

## 8. Top Inspection Findings (Bar Chart)

### Overview

**Component**: `ShadcnBarCard`  
**Title**: "Top Inspection Findings"  
**Purpose**: Lists the most commonly identified issues during safety inspections

### Data Source

**Sheet**: `Inspection`

**Columns Used** (same preference order as audits):

1. `finding` OR `findings`
2. `observation` OR `observations`
3. `non_conformance` OR `non conformance`
4. `issue` OR `issues`
5. `remark` OR `remarks`
6. `description`
7. `checklist_category` OR `checklist category` (fallback)

**Backend Endpoint**: `/analytics/data/inspection-top-findings`

**Query Parameters**: Same as audit findings

### Calculation Formula

**Identical logic to Audit Findings** (see section 7)

The same cleaning, filtering, and aggregation process applies.

### Example Response

```json
{
  "labels": [
    "Housekeeping poor",
    "Safety glasses not worn",
    "Tools not stored properly",
    "Spill not cleaned",
    "Ladder damaged",
    "Extension cords misused"
  ],
  "series": [
    {
      "name": "Count",
      "data": [62, 55, 48, 42, 38, 31]
    }
  ]
}
```

### Key Differences from Audit Findings

- **Source data**: Inspection sheet (routine checks) vs Audit sheet (formal assessments)
- **Frequency**: Inspections are more frequent, so typically higher counts
- **Detail level**: Inspection findings tend to be more operational (housekeeping, PPE) vs audits (systemic gaps, compliance)

### Filter Support

✅ Same as Audit Findings

### Visualization

- **Type**: Horizontal bar chart
- **Limit**: Top 20 findings
- **Color**: Primary theme color

---

## 9. Department × Month Heatmap

### Overview

**Component**: `ShadcnHeatmapCard`  
**Title**: "Department × Month (Avg)"  
**Purpose**: Shows average risk/severity scores by department and month to identify patterns

### Data Source

**Sheet**: `Incident`

**Columns Used**:

- `Department` OR `Section`
- `Date of Occurrence` OR `Date Reported` (for month extraction)
- `risk_score` OR `severity_score` (for metric calculation, optional)

**Backend Endpoint**: `/analytics/data/department-month-heatmap`

**Query Parameters**:

```javascript
{
  dataset: "incident",
  start_date: "YYYY-MM-DD",
  end_date: "YYYY-MM-DD",
  departments: [...],
  locations: [...],
  min_severity: 0,
  max_severity: 5,
  min_risk: 0,
  max_risk: 5
}
```

### Calculation Formula

```python
def calculate_department_month_heatmap(incident_df, filters):
    # 1. Apply filters
    filtered_df = apply_analytics_filters(incident_df, **filters)

    # 2. Find columns
    dept_col = resolve_column(filtered_df, ["department", "section"])
    date_col = resolve_column(filtered_df, [
        "occurrence_date",
        "date of occurrence",
        "date reported"
    ])

    # 3. Convert dates to monthly periods (YYYY-MM format)
    months = pd.to_datetime(filtered_df[date_col], errors='coerce')
    months = months.dt.to_period('M').astype(str)

    # 4. Find metric column (optional)
    metric_col = resolve_column(filtered_df, ["risk_score", "severity_score"])

    # 5. Build pivot table
    pivot_data = pd.DataFrame({
        "department": filtered_df[dept_col].astype(str),
        "month": months
    })

    if metric_col is not None:
        # Calculate AVERAGE of risk/severity scores
        pivot_data["value"] = pd.to_numeric(
            filtered_df[metric_col],
            errors='coerce'
        )
        pivot = pivot_data.pivot_table(
            values="value",
            index="department",
            columns="month",
            aggfunc="mean"  # Average
        )
        metric = "avg"
    else:
        # COUNT of incidents
        pivot_data["value"] = 1
        pivot = pivot_data.pivot_table(
            values="value",
            index="department",
            columns="month",
            aggfunc="count"  # Count
        )
        metric = "count"

    # 6. Format for heatmap
    x_labels = [str(c) for c in pivot.columns]  # Months (YYYY-MM)
    y_labels = [str(i) for i in pivot.index]    # Departments
    z_values = pivot.fillna(0).to_numpy().tolist()  # Matrix values

    return {
        "x": x_labels,      # Months (columns)
        "y": y_labels,      # Departments (rows)
        "z": z_values,      # 2D array of values
        "metric": metric    # "avg" or "count"
    }
```

### Metric Calculation

```python
# If risk_score or severity_score column exists:
metric = MEAN(scores per department-month cell)

# If no score column exists:
metric = COUNT(incidents per department-month cell)
```

### Example Response

```json
{
  "x": ["2023-01", "2023-02", "2023-03", "2023-04"],
  "y": ["Production", "Maintenance", "Technical", "Commercial"],
  "z": [
    [2.5, 3.1, 2.8, 3.5], // Production scores/counts
    [1.8, 2.2, 1.5, 2.0], // Maintenance
    [3.2, 3.8, 4.1, 3.6], // Technical
    [1.2, 1.5, 1.8, 1.3] // Commercial
  ],
  "metric": "avg"
}
```

### Color Scale

```javascript
// For heatmap visualization
const colorScale = d3
  .scaleSequential(d3.interpolateYlOrRd)
  .domain([0, maxValue])

// Light = low values (green/yellow)
// Dark = high values (orange/red)
```

### Monthly Granularity

Dates are converted to month periods:

```python
# Input: "2023-05-15"
# Output: "2023-05"

dt = pd.to_datetime(date_column)
month_period = dt.dt.to_period('M').astype(str)
```

### Filter Support

✅ **Filters apply**:

- Date range
- Departments (limits rows)
- Locations
- Min/max severity
- Min/max risk

### Visualization

- **Type**: Heatmap matrix
- **Rows**: Departments (y-axis)
- **Columns**: Months (x-axis)
- **Color intensity**: Represents value (light → dark)
- **Tooltip**: Shows department, month, exact value
- **Color scheme**: Yellow-Orange-Red gradient

---

## 10. Recent Items Lists

### Overview

**Component**: `RecentList`  
**Purpose**: Display the 5 most recent items for quick reference

### 10.1 Recent Incidents

**Data Source**:

- **Sheet**: `Incident`
- **Columns**:
  - `Incident Number` (ID format: IN-YYYYMMDD-NNN)
  - `Title` OR `Description`
  - `Department`
  - `Status`
  - `Date of Occurrence` OR `Date Reported` OR `Date Entered` (for sorting)

**Backend Endpoint**: `/data/incidents/recent?limit=5`

**Formula**:

```python
def get_recent_incidents(limit=5):
    # 1. Load incident DataFrame
    df = get_incident_df()

    # 2. Find best date column for sorting
    date_col = resolve_column(df, [
        "Date of Occurrence",
        "occurrence_date",
        "Date Reported",
        "Date Entered"
    ])

    # 3. Convert to datetime and sort descending
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df_sorted = df[df[date_col].notna()].sort_values(
        by=date_col,
        ascending=False
    ).head(limit)

    # 4. Extract fields
    return [
        {
            "id": row["Incident Number"],
            "title": row["Title"],
            "department": row["Department"],
            "status": row["Status"],
            "date": row[date_col].strftime('%Y-%m-%d')
        }
        for _, row in df_sorted.iterrows()
    ]
```

**Example Response**:

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
    "title": "Agitator moved during vessel entry",
    "department": "PVC",
    "status": "Closed",
    "date": "2023-01-02"
  }
]
```

---

### 10.2 Recent Hazards

**Data Source**:

- **Sheet**: `Hazard ID`
- **Columns**:
  - `hazard_id` (or generated: HAZ-NNN)
  - `Title` OR `Description`
  - `Status`
  - `Date Entered` OR `Date Reported` (for sorting)

**Backend Endpoint**: `/data/hazards/recent?limit=5`

**Formula**: Similar to Recent Incidents, but uses hazard-specific date columns

**Example Response**:

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

---

### 10.3 Recent Audits

**Data Source**:

- **Sheet**: `Audit`
- **Columns**:
  - `audit_id` (or generated: AUD-NNN)
  - `Title` OR `audit_title`
  - `Status` OR `audit_status`
  - `scheduled_date` OR `start_date` (for sorting)

**Backend Endpoint**: `/data/audits/recent?limit=5`

**Formula**: Similar to above, uses audit-specific date columns

**Example Response**:

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

## Global Filters

All charts (except Recent Items) support the following filters:

### Filter Parameters

| Parameter         | Type   | Description               | Example                            |
| ----------------- | ------ | ------------------------- | ---------------------------------- |
| `start_date`      | string | Start date (YYYY-MM-DD)   | "2023-01-01"                       |
| `end_date`        | string | End date (YYYY-MM-DD)     | "2023-12-31"                       |
| `departments`     | array  | Filter by departments     | ["Production", "Maintenance"]      |
| `locations`       | array  | Filter by locations       | ["Karachi", "Lahore"]              |
| `sublocations`    | array  | Filter by sublocations    | ["Manufacturing Facility"]         |
| `statuses`        | array  | Filter by status          | ["Open", "Closed"]                 |
| `incident_types`  | array  | Filter by incident types  | ["Injury", "Property Damage"]      |
| `violation_types` | array  | Filter by violation types | ["Unsafe Act", "Unsafe Condition"] |
| `min_severity`    | number | Minimum severity (0-5)    | 2.0                                |
| `max_severity`    | number | Maximum severity (0-5)    | 4.0                                |
| `min_risk`        | number | Minimum risk (0-5)        | 1.0                                |
| `max_risk`        | number | Maximum risk (0-5)        | 3.0                                |

### Filter Application Logic

```python
def apply_analytics_filters(df, **filters):
    filtered = df.copy()

    # Date range filter
    if filters.get('start_date') or filters.get('end_date'):
        date_col = resolve_date_column(filtered)
        dates = pd.to_datetime(filtered[date_col], errors='coerce')

        if filters.get('start_date'):
            mask = dates >= pd.to_datetime(filters['start_date'])
            filtered = filtered[mask]

        if filters.get('end_date'):
            mask = dates <= pd.to_datetime(filters['end_date'])
            filtered = filtered[mask]

    # Department filter
    if filters.get('departments'):
        dept_col = resolve_column(filtered, ["department", "section"])
        filtered = filtered[filtered[dept_col].isin(filters['departments'])]

    # Location filter
    if filters.get('locations'):
        loc_col = resolve_column(filtered, ["location"])
        filtered = filtered[filtered[loc_col].isin(filters['locations'])]

    # Severity range filter
    if filters.get('min_severity') or filters.get('max_severity'):
        sev_col = resolve_column(filtered, ["severity_score", "severity"])
        severity = pd.to_numeric(filtered[sev_col], errors='coerce')

        if filters.get('min_severity'):
            filtered = filtered[severity >= filters['min_severity']]
        if filters.get('max_severity'):
            filtered = filtered[severity <= filters['max_severity']]

    # ... (similar logic for other filters)

    return filtered
```

---

## Summary Table

| Chart Name               | Data Source (Sheet)                            | Key Columns                                                                     | Endpoint                                                       | Granularity                             | Filter Support           |
| ------------------------ | ---------------------------------------------- | ------------------------------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------- | ------------------------ | ------ |
| **KPI Cards**            | Incident, Hazard, Audit, Inspection            | Unique non-null IDs (Incident Number/Audit Number; hazards use Incident Number) | `/data-health/counts/all`                                      | N/A                                     | ❌ None                  |
| **Hazards Trend**        | Hazard ID                                      | Date Entered, all rows                                                          | `/analytics/data/incident-trend-detailed`                      | Daily                                   | ✅ All + per-chart dates |
| **Incidents Trend**      | Incident                                       | Date of Occurrence, all rows                                                    | `/analytics/data/incident-trend-detailed`                      | Daily                                   | ✅ All + per-chart dates |
| **Root Cause Pareto**    | Incident                                       | Root Cause, Incident Type(s)                                                    | `/analytics/data/root-cause-pareto`                            | N/A                                     | ✅ All + incident type   |
| **Hazards by Type**      | Hazard ID                                      | Incident Type(s)                                                                | `/analytics/data/hazard-top-findings`                          | N/A                                     | ✅ All                   |
|                          | **Incidents by Type and Severity (Hazard ID)** | Hazard ID                                                                       | Incident Type(s), Worst Case Consequence Potential (Hazard ID) | `/analytics/data/incident-top-findings` | N/A                      | ✅ All |
| **Audit Findings**       | Audit                                          | finding/observation/description                                                 | `/analytics/data/audit-top-findings`                           | N/A                                     | ✅ Most                  |
| **Inspection Findings**  | Inspection                                     | finding/observation/description                                                 | `/analytics/data/inspection-top-findings`                      | N/A                                     | ✅ Most                  |
| **Dept × Month Heatmap** | Incident                                       | Department, Date, risk_score                                                    | `/analytics/data/department-month-heatmap`                     | Monthly                                 | ✅ All                   |
| **Recent Incidents**     | Incident                                       | Incident Number, Title, Status, Date                                            | `/data/incidents/recent`                                       | N/A                                     | ❌ None                  |
| **Recent Hazards**       | Hazard ID                                      | hazard_id, Title, Status, Date                                                  | `/data/hazards/recent`                                         | N/A                                     | ❌ None                  |
| **Recent Audits**        | Audit                                          | audit_id, Title, Status, Date                                                   | `/data/audits/recent`                                          | N/A                                     | ❌ None                  |

---

## Technical Architecture

### Frontend Flow

```
User Interaction
     ↓
Filter State Update (React State)
     ↓
Build Query Parameters
     ↓
API Call (React Query / useCachedGet)
     ↓
Backend Endpoint
     ↓
Response (JSON)
     ↓
Chart Component Rendering
     ↓
Visualization (Recharts / Shadcn)
```

### Backend Flow

```
API Endpoint Receives Request
     ↓
Parse Query Parameters
     ↓
Load Excel Data (Cached)
     ↓
Apply Filters (apply_analytics_filters)
     ↓
Resolve Column Names (_resolve_column)
     ↓
Data Processing & Aggregation
     ↓
Format Response (JSON)
     ↓
Return to Frontend
```

### Caching Strategy

**Frontend**:

- React Query with stale/gcTime settings
- 6 hours TTL for KPI summary
- Infinite cache for data health counts
- Refresh via `refreshKey` state

**Backend**:

- Excel data loaded once and cached (`@lru_cache`)
- Filters applied dynamically on cached data
- No database queries (pure in-memory processing)

---

## Performance Considerations

### Data Volume

| Dataset    | Typical Rows            | Columns | Load Time |
| ---------- | ----------------------- | ------- | --------- |
| Incident   | 866 valid / 2,596 total | 169     | < 1s      |
| Hazard ID  | ~500-1000               | 50-100  | < 1s      |
| Audit      | ~100-500                | 30-50   | < 1s      |
| Inspection | ~1000-5000              | 30-50   | < 1s      |

### Optimization Techniques

1. **Column Resolution**: Flexible column name matching
2. **Vectorized Operations**: Pandas for fast aggregations
3. **Smart Filtering**: Filter early to reduce data size
4. **Caching**: LRU cache for Excel data loading
5. **Lazy Evaluation**: Data loaded only when endpoints called

### Response Times

- **KPI Cards**: < 100ms
- **Trend Charts**: < 200ms
- **Pareto/Bar Charts**: < 300ms
- **Heatmap**: < 500ms (due to pivot table)
- **Recent Items**: < 100ms

---

## Backend Verification Summary (all Overview charts)

- Hazards Trend (Line)

  - Component: ShadcnLineCardEnhanced
  - Endpoint: /analytics/data/incident-trend-detailed (dataset=hazard)
  - Backend: routers/analytics_general.py:data_incident_trend_detailed
  - Columns: date from [occurrence_date | date of occurrence | date reported | date entered]
  - Aggregation: daily counts (value_counts sorted by date)
  - Filters: applied via services/filters.py:apply_analytics_filters

- Incidents Trend (Line)

  - Same endpoint with dataset=incident; same logic, type column resolved for incident version

- Root Cause Pareto (Bars + Line)

  - Endpoint: /analytics/data/root-cause-pareto (+ /incident-types for radio options)
  - Backend: routers/analytics_general.py:data_root_cause_pareto
  - Columns: Root cause from [Root Cause | root_cause | Key Factor | key_factor | Contributing Factor | contributing_factor]
  - Logic: split on ';', clean placeholders, count top N, cumulative % line
  - Filters: standard filters + optional incident_type (case-insensitive exact match after splitting)

- Hazards by Incident Type Category (Bar)

  - Endpoint: /analytics/data/hazard-top-findings
  - Backend: routers/analytics_general.py:data_hazard_top_findings
  - Columns: Incident Type(s) from [incident_type(s) | incident type(s) | incident_types | incident type | incident_type]
  - Logic: clean whitespace/NA; counts ALL categories (combined tokens like "A; B" treated as one label)
  - Filters: applied

- Incidents by Type and Severity (Stacked Bar)

  - Endpoint: /analytics/data/incident-top-findings
  - Backend: routers/analytics_general.py:data_incident_top_findings
  - Dataset used: Hazard sheet
  - Columns: Incident Type(s) as above; Severity: Worst Case Consequence Potential (Hazard ID) (flexible match)
  - Logic: clean, drop NA, group incident types < min_count (default 8) into "Others"; crosstab type × severity; ensure severity columns C0..C3; sort by totals
  - Filters: applied

- Top Audit Findings (Bar)

  - Endpoint: /analytics/data/audit-top-findings
  - Backend: routers/analytics_general.py:data_audit_top_findings
  - Columns: prefer [finding/findings | observation(s) | non_conformance | issue(s) | remark(s) | description | checklist_category]
  - Logic: normalize whitespace, strip punctuation, drop NA/"No finding" patterns; if category field used, split by ';' or ',' then re-normalize; top 20 tokens
  - Filters: applied

- Top Inspection Findings (Bar)

  - Endpoint: /analytics/data/inspection-top-findings
  - Backend: routers/analytics_general.py:data_inspection_top_findings
  - Logic: identical to Audit Findings but on Inspection dataset

- Department × Month Heatmap

  - Endpoint: /analytics/data/department-month-heatmap
  - Backend: routers/analytics_general.py:data_department_month_heatmap
  - Columns: department (fallback: section); date month from [occurrence_date | date of occurrence | date reported]
  - Metric: avg if risk_score/severity_score exists, else count
  - Filters: applied

- Recent Lists (Incidents/Hazards/Audits)

  - Endpoints: /incidents/recent, /hazards/recent, /audits/recent
  - Backend: routers/data.py:list_recent_incidents|list_recent_hazards|list_recent_audits
  - Logic: choose best available date per dataset, drop null, sort desc, return top N

- KPI Totals (6 cards)
  - Endpoint: /data-health/counts/all
  - Backend: routers/data_health.py:get_all_counts
  - Logic: global totals only (filters ignored); counts unique non-null IDs
    - Incident: Incident Number
    - Hazard: Incident Number (current implementation)
    - Audit: Audit Number
    - Inspection: Audit Number
    - Audit Findings / Inspection Findings: pick sheets by name tokens ("audit find*", "inspection find*") and count unique Audit Number (represents audits/inspections with ≥1 finding)

## KPI Counting Behavior (authoritative)

- KPIs are computed as unique, non-null ID counts and ignore filters entirely.
- Hazards KPI currently uses the "Incident Number" column from the Hazard sheet; if you want "Hazard ID" counting, we can update the backend column selection.
- Findings KPIs count distinct audit/inspection records with findings (not the total number of finding rows). We can change this to count finding rows if desired.

## Filters Implementation Reference

- File: services/filters.py:apply_analytics_filters
- Supported filters and column resolution:
  - Date range: tries multiple date columns; compares with >= start_date and <= end_date
  - Departments: department (case-insensitive); fallback handling present across datasets
  - Locations: first existing in [location, location.1, site]
  - Sublocations: sublocation
  - Severity range: first in [severity_score, severity, severity_level], numeric compare
  - Risk range: first in [risk_score, risk, risk_level], numeric compare
  - Statuses: status exact (case-insensitive)
  - Incident types: match if any selected type appears within the string; handles multi-value fields
  - Violation types: same strategy as incident types

## Recommendations

1. If you need KPIs to reflect current filters (date, department, etc.), extend /data-health/counts/all to accept those parameters and reuse apply_analytics_filters.
2. Switch Hazards KPI to a dedicated Hazard ID/Hazard Number column if available for accuracy.
3. For Findings KPIs, decide whether you want counts of distinct audits/inspections with findings (current) or total number of findings rows; adjust logic accordingly.

## Conclusion

This report documents all 12 chart types in the Overview section, providing complete transparency into:

- **Data sources** (Excel sheets and specific columns)
- **Calculation formulas** (Python/Pandas logic)
- **API endpoints** (backend routes)
- **Filter capabilities** (what can be filtered and how)
- **Visualization details** (chart types, colors, interactivity)

All charts follow a consistent pattern:

1. Load data from Excel sheets
2. Apply global and per-chart filters
3. Resolve column names flexibly
4. Aggregate/calculate metrics
5. Format as JSON for frontend
6. Render using Recharts/Shadcn components

This architecture provides a robust, maintainable, and performant analytics dashboard for HSE data visualization.
