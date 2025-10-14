# Overview Charts Backend Verification Report

This document verifies every chart in the Overview page against the backend implementation and summarizes the exact data sources, columns, and formulas used.

Repository paths used below are relative to `server/app`.

---

## 1) Hazards Trend (Line)
- Frontend component: `ShadcnLineCardEnhanced`
- Frontend source: `client/src/pages/Overview.tsx`
  - Calls endpoint: `/analytics/data/incident-trend-detailed`
  - Params: `{ dataset: "hazard", ...filters }`
- Backend endpoint: `routers/analytics_general.py:data_incident_trend_detailed`
- Column resolution and logic (verified):
  - Date column: first match in [`occurrence_date`, `date of occurrence`, `date reported`, `date entered`]
  - Granularity: Daily (YYYY-MM-DD)
  - Count per day via `value_counts().sort_index()`
  - Filters applied via `services/filters.py:apply_analytics_filters`
  - Details returned per day: top departments, top types (violation types for hazard), severity/risk stats, up to 5 recent items

## 2) Incidents Trend (Line)
- Calls same endpoint: `/analytics/data/incident-trend-detailed`
- Params: `{ dataset: "incident", ...filters }`
- Backend and formula: Same function as hazards trend, with incident-specific type column resolution:
  - Type column picks from [`incident type(s)`, `incident_type(s)`, `incident_type`, `category`, `accident type`]

## 3) Root Cause Pareto (Bars + Line)
- Frontend component: `ShadcnParetoCard`
- Endpoint: `/analytics/data/root-cause-pareto`
- Backend: `routers/analytics_general.py:data_root_cause_pareto`
- Verified logic:
  - Filters applied via `apply_analytics_filters`
  - Optional incident_type radio filter: splits `incident_type(s)` on `;` and performs case-insensitive exact match
  - Root cause column: first present in [`Root Cause`, `root_cause`, `Key Factor`, `key_factor`, `Contributing Factor`, `contributing_factor`]
  - Splits root cause values on `;`, trims, removes NA/placeholder text
  - Counts top N (default 15)
  - Cumulative percent = `counts.cumsum() / counts.sum() * 100`
- Extra endpoint for radio options: `/analytics/data/root-cause-pareto/incident-types`

## 4) Hazards by Incident Type Category (Bar)
- Frontend component: `ShadcnBarCard`
- Endpoint: `/analytics/data/hazard-top-findings`
- Backend: `routers/analytics_general.py:data_hazard_top_findings`
- Verified logic:
  - Filters applied via `apply_analytics_filters`
  - Incident type column seekers: [`incident_type(s)`, `incident type(s)`, `incident_types`, `incident type`, `incident_type`]
  - Cleans whitespace and placeholders, counts values as-is (combined multi-values like `A; B` are treated as one category), returns ALL categories (sorted desc).

## 5) Incidents by Type and Severity (Stacked Bar)
- Frontend component: `StackedBarCard`
- Endpoint: `/analytics/data/incident-top-findings`
- Backend: `routers/analytics_general.py:data_incident_top_findings`
- Verified logic (Important: uses Hazard sheet):
  - Dataset used: Hazard DataFrame
  - Filters applied via `apply_analytics_filters`
  - Columns:
    - Incident Type(s): same seekers as above, cleaned
    - Severity: `Worst Case Consequence Potential (Hazard ID)` via flexible matching; cleaned
  - Drops rows missing incident type or severity
  - Groups incident types with counts < `min_count` (default 8) into `Others`
  - Crosstab (incident type × severity)
  - Severity order restricted to `C0`..`C3` for Hazard ID sheet
  - Adds missing severities with zeros, sorts rows by total desc and returns stacked series + totals

## 6) Top Audit Findings (Bar)
- Frontend component: `ShadcnBarCard`
- Endpoint: `/analytics/data/audit-top-findings`
- Backend: `routers/analytics_general.py:data_audit_top_findings`
- Verified logic:
  - Filters applied via `apply_analytics_filters`
  - Column priority list (first existing):
    - `finding`/`findings`, `observation`/`observations`, `non_conformance`/`non conformance`, `issue`/`issues`, `remark`/`remarks`, `description`, fallback to `checklist_category`
  - Text normalization: condense whitespace, strip punctuation, drop `N/A`/`No findings`-like placeholders
  - If using a category column, splits on `;` or `,`, re-normalizes tokens
  - Value counts of tokens, Top 20 returned (labels + counts)

## 7) Top Inspection Findings (Bar)
- Frontend component: `ShadcnBarCard`
- Endpoint: `/analytics/data/inspection-top-findings`
- Backend: `routers/analytics_general.py:data_inspection_top_findings`
- Verified logic: Identical to Audit Findings, but uses the Inspection dataset accessor

## 8) Department × Month Heatmap
- Frontend component: `ShadcnHeatmapCard`
- Endpoint: `/analytics/data/department-month-heatmap`
- Backend: `routers/analytics_general.py:data_department_month_heatmap`
- Verified logic:
  - Dataset: Incident (or hazard if dataset param passed), filters via `apply_analytics_filters`
  - Department column: `department` (fallback: `section`)
  - Date column: first in [`occurrence_date`, `date of occurrence`, `date reported`]
  - Month aggregation: period to `YYYY-MM`
  - Metric:
    - If `risk_score` or `severity_score` exists: pivot with `mean` (returns metric=`avg`)
    - Else: pivot with `count` (returns metric=`count`)
  - Returns x (months), y (departments), z (matrix)

## 9) Recent Lists (Incidents/Hazards/Audits)
- Frontend component: `RecentList`
- Endpoints:
  - `/incidents/recent?limit=N`
  - `/hazards/recent?limit=N`
  - `/audits/recent?limit=N`
- Backend: `routers/data.py` functions `list_recent_incidents`, `list_recent_hazards`, `list_recent_audits`
- Verified logic:
  - Sort by best-available date column (incidents: `Date of Occurrence` → `Date Reported` → `Date Entered`; hazards: `Date Entered` → `Date Reported` → `occurrence_date`; audits: `scheduled_date` → `start_date`)
  - Drop null dates and sort descending; return top `limit`
  - Return fields: id, title, status (and department for incidents), date (ISO)

## 10) KPI Totals (6 cards)
- Endpoint: `/data-health/counts/all`
- Backend: `routers/data_health.py:get_all_counts`
- Verified logic:
  - Global totals; filters are ignored
  - Counts unique, non-null IDs per dataset:
    - Incident: `Incident Number`
    - Hazard: `Incident Number` (current implementation)
    - Audit: `Audit Number`
    - Inspection: `Audit Number`
  - Findings KPIs: choose findings sheets by name tokens (`audit find*`, `inspection find*`), then count unique non-null `Audit Number` on those sheets (audits or inspections with findings, not raw finding rows)

---

## Filters Behavior (applies to all analytics charts above)
- Implemented in: `services/filters.py:apply_analytics_filters`
- Supported parameters (case-insensitive matching, robust column resolution):
  - Date range: tries multiple date columns and filters `>= start_date` and `<= end_date`
  - Departments: exact match on `department` (case-insensitive)
  - Locations: first available in [`location`, `location.1`, `site`]
  - Sublocations: `sublocation`
  - Severity range: first available in [`severity_score`, `severity`, `severity_level`], numeric compare
  - Risk range: first available in [`risk_score`, `risk`, `risk_level`]
  - Statuses: `status`
  - Incident Types: tries several columns and matches if any selected type occurs in the string (handles multi-values)
  - Violation Types: same strategy for hazard fields

---

## Notes & Recommendations
1) KPI totals are global: the endpoint currently ignores filters and uses unique IDs. If filtered KPIs are desired, extend `/data-health/counts/all` to accept and apply the same filters used by analytics endpoints.
2) Hazards KPI uses `Incident Number` today. If a dedicated `Hazard ID/Hazard Number` exists, update the KPI counting column for better accuracy.
3) Findings KPIs count audits/inspections with findings (unique `Audit Number`). If the desired metric is total finding rows, change the logic to count non-empty finding/observation/description records (or a `Finding ID` if present).

---

All items above have been verified against the code in `routers/analytics_general.py`, `routers/data.py`, `routers/data_health.py`, and `services/filters.py` at the time of this report.
