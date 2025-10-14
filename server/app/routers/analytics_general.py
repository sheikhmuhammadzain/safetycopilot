from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import json
import re
import numpy as np
import pandas as pd
from typing import Optional, List, Dict

from ..models.schemas import (
    PlotlyFigureResponse,
    ChartInsightsRequest,
    ChartInsightsResponse,
    DataInsightsRequest,
    AnalyticsFilters,
    FilterOptionsResponse,
    CombinedFilterOptionsResponse,
    DetailedTrendResponse,
    MonthDetailedData,
    CountItem,
    ScoreStats,
    RecentItem,
    ChartSeries,
)
from ..services.excel import (
    get_incident_df,
    get_hazard_df,
    get_audit_df,
    get_inspection_df,
)
from ..services import plots as plot_service
from ..services.json_utils import to_native_json
from ..services.agent import ask_openai
from ..services.excel import payload_to_df
from ..services.insights_generator import PlotlyInsightsGenerator, InsightType
from ..services.filters import apply_analytics_filters, get_filter_summary
from ..services.filter_options import extract_filter_options, extract_combined_filter_options


router = APIRouter(prefix="/analytics", tags=["analytics"])


def _resolve_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    if df is None or df.empty:
        return None
    colmap = {str(c).strip().lower(): c for c in df.columns}
    for cand in candidates:
        k = str(cand).strip().lower()
        if k in colmap:
            return colmap[k]
    # try relaxed contains match
    for cand in candidates:
        k = str(cand).strip().lower()
        for lk, orig in colmap.items():
            if k in lk:
                return orig
    return None


def _to_date_period(series: pd.Series, granularity: str = 'D') -> pd.Series:
    """
    Convert datetime series to period strings.
    
    Args:
        series: Pandas series with datetime values
        granularity: 'D' for daily (YYYY-MM-DD), 'M' for monthly (YYYY-MM)
    
    Returns:
        Series with period strings
    """
    dt = pd.to_datetime(series, errors='coerce')
    if granularity == 'M':
        return dt.dt.to_period('M').astype(str)
    else:  # Daily by default
        return dt.dt.date.astype(str)


@router.get("/hse-scorecard", response_model=PlotlyFigureResponse)
async def hse_scorecard():
    inc = get_incident_df()
    haz = get_hazard_df()
    aud = get_audit_df()
    ins = get_inspection_df()
    fig = plot_service.create_unified_hse_scorecard(inc, haz, aud, ins)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/filter-options", response_model=FilterOptionsResponse)
async def get_filter_options(
    dataset: str = Query("incident", description="Dataset to use: 'incident' or 'hazard'")
):
    """
    Get all available filter options for a specific dataset.
    Returns unique values for departments, locations, statuses, types, etc.
    Useful for populating frontend dropdown menus and filter UI components.
    
    Example:
        GET /analytics/filter-options?dataset=incident
        
    Returns:
        - Date range (min/max dates)
        - Available departments with counts
        - Available locations with counts
        - Available statuses with counts
        - Available incident/violation types with counts
        - Severity and risk score ranges
    """
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    options = extract_filter_options(df, dataset)
    return options


@router.get("/filter-options/combined", response_model=CombinedFilterOptionsResponse)
async def get_combined_filter_options():
    """
    Get all available filter options from both incident and hazard datasets.
    Returns comprehensive filter options for building a unified filter UI.
    
    Example:
        GET /analytics/filter-options/combined
        
    Returns:
        - Filter options for incidents
        - Filter options for hazards
        - Timestamp of when options were generated
    """
    incident_df = get_incident_df()
    hazard_df = get_hazard_df()
    combined_options = extract_combined_filter_options(incident_df, hazard_df)
    return combined_options


@router.get("/filter-summary")
async def get_filter_summary_endpoint(
    dataset: str = Query("incident", description="Dataset to use: 'incident' or 'hazard'"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    min_severity: Optional[float] = Query(None, ge=0, le=5, description="Min severity"),
    max_severity: Optional[float] = Query(None, ge=0, le=5, description="Max severity"),
    min_risk: Optional[float] = Query(None, ge=0, le=5, description="Min risk"),
    max_risk: Optional[float] = Query(None, ge=0, le=5, description="Max risk"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
    incident_types: Optional[List[str]] = Query(None, description="Filter by incident types"),
    violation_types: Optional[List[str]] = Query(None, description="Filter by violation types"),
):
    """
    Get a summary of how filters would affect the dataset without returning the full data.
    Useful for UI to show filter impact before applying to charts.
    """
    df_original = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    df_filtered = apply_analytics_filters(
        df_original,
        start_date=start_date,
        end_date=end_date,
        departments=departments,
        locations=locations,
        sublocations=sublocations,
        min_severity=min_severity,
        max_severity=max_severity,
        min_risk=min_risk,
        max_risk=max_risk,
        statuses=statuses,
        incident_types=incident_types,
        violation_types=violation_types,
    )
    
    filters_dict = {
        'dataset': dataset,
        'start_date': start_date,
        'end_date': end_date,
        'departments': departments,
        'locations': locations,
        'sublocations': sublocations,
        'min_severity': min_severity,
        'max_severity': max_severity,
        'min_risk': min_risk,
        'max_risk': max_risk,
        'statuses': statuses,
        'incident_types': incident_types,
        'violation_types': violation_types,
    }
    
    summary = get_filter_summary(df_original, df_filtered, filters_dict)
    
    return JSONResponse(content=summary)


# ----------------------- DATA (JSON) ENDPOINTS FOR FRONTEND --------------------

@router.get("/data/incident-trend")
async def data_incident_trend(
    dataset: str = Query("incident"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    min_severity: Optional[float] = Query(None, ge=0, le=5, description="Min severity"),
    max_severity: Optional[float] = Query(None, ge=0, le=5, description="Max severity"),
    min_risk: Optional[float] = Query(None, ge=0, le=5, description="Min risk"),
    max_risk: Optional[float] = Query(None, ge=0, le=5, description="Max risk"),
):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply flexible filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, min_severity=min_severity, max_severity=max_severity,
        min_risk=min_risk, max_risk=max_risk
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    date_col = _resolve_column(df, ["occurrence_date", "date of occurrence", "date reported", "date entered"]) or df.columns[0]
    dates = _to_date_period(df[date_col], granularity='D')  # Daily granularity
    counts = dates.value_counts().sort_index()
    return JSONResponse(content={
        "labels": counts.index.tolist(),
        "series": [{"name": "Count", "data": counts.values.astype(int).tolist()}],
    })


@router.get("/data/incident-trend-detailed", response_model=DetailedTrendResponse)
async def data_incident_trend_detailed(
    dataset: str = Query("incident", description="Dataset to use: 'incident' or 'hazard'"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    min_severity: Optional[float] = Query(None, ge=0, le=5, description="Min severity"),
    max_severity: Optional[float] = Query(None, ge=0, le=5, description="Max severity"),
    min_risk: Optional[float] = Query(None, ge=0, le=5, description="Min risk"),
    max_risk: Optional[float] = Query(None, ge=0, le=5, description="Max risk"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
    incident_types: Optional[List[str]] = Query(None, description="Filter by incident types"),
    violation_types: Optional[List[str]] = Query(None, description="Filter by violation types"),
):
    """
    Enhanced endpoint that returns trend data WITH detailed breakdowns for tooltips.
    
    Returns:
    - labels: Date labels (YYYY-MM-DD format)
    - series: Chart data (counts per day)
    - details: Detailed breakdown per day including:
        - Top departments with counts
        - Top incident/violation types with counts
        - Severity and risk statistics
        - Recent items (up to 5 most recent)
    
    Example:
        GET /analytics/data/incident-trend-detailed?dataset=incident&start_date=2023-01-01
    """
    # Load dataset
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply filters
    df = apply_analytics_filters(
        df, 
        start_date=start_date, 
        end_date=end_date, 
        departments=departments,
        locations=locations, 
        sublocations=sublocations,
        min_severity=min_severity, 
        max_severity=max_severity,
        min_risk=min_risk, 
        max_risk=max_risk,
        statuses=statuses,
        incident_types=incident_types,
        violation_types=violation_types,
    )
    
    if df is None or df.empty:
        return DetailedTrendResponse(labels=[], series=[], details=[])
    
    # Resolve column names
    date_col = _resolve_column(df, ["occurrence_date", "date of occurrence", "date reported", "date entered"]) or df.columns[0]
    dept_col = _resolve_column(df, ["department", "section"]) or None
    title_col = _resolve_column(df, ["title", "description", "incident description", "hazard description"]) or None
    severity_col = _resolve_column(df, ["severity_score", "severity", "actual consequence (incident)"]) or None
    risk_col = _resolve_column(df, ["risk_score", "risk"]) or None
    
    # Type column depends on dataset
    if (dataset or "incident").lower() == "incident":
        type_col = _resolve_column(df, ["incident type(s)", "category", "accident type"]) or None
    else:
        type_col = _resolve_column(df, ["violation type (hazard)", "violation_type_hazard_id", "category"]) or None
    
    # Convert dates to daily periods
    df_copy = df.copy()
    df_copy['_day'] = _to_date_period(df_copy[date_col], granularity='D')  # Daily granularity
    df_copy['_date'] = pd.to_datetime(df_copy[date_col], errors='coerce')
    
    # Get overall counts
    days = df_copy['_day']
    counts = days.value_counts().sort_index()
    
    # Build detailed breakdown for each day
    details = []
    for day_label in counts.index:
        day_df = df_copy[df_copy['_day'] == day_label]
        total_count = len(day_df)
        
        # Top departments
        departments_list = []
        if dept_col and dept_col in day_df.columns:
            dept_counts = day_df[dept_col].astype(str).value_counts().head(5)
            departments_list = [
                CountItem(name=str(dept), count=int(count))
                for dept, count in dept_counts.items()
            ]
        
        # Top types
        types_list = []
        if type_col and type_col in day_df.columns:
            # Handle comma-separated values
            type_series = day_df[type_col].astype(str).str.split(',').explode().str.strip()
            type_counts = type_series.value_counts().head(5)
            types_list = [
                CountItem(name=str(t), count=int(count))
                for t, count in type_counts.items()
                if str(t).lower() not in ['nan', 'none', '']
            ]
        
        # Severity stats
        severity_stats = None
        if severity_col and severity_col in day_df.columns:
            sev_values = pd.to_numeric(day_df[severity_col], errors='coerce').dropna()
            if len(sev_values) > 0:
                severity_stats = ScoreStats(
                    avg=float(sev_values.mean()),
                    max=float(sev_values.max()),
                    min=float(sev_values.min())
                )
        
        # Risk stats
        risk_stats = None
        if risk_col and risk_col in day_df.columns:
            risk_values = pd.to_numeric(day_df[risk_col], errors='coerce').dropna()
            if len(risk_values) > 0:
                risk_stats = ScoreStats(
                    avg=float(risk_values.mean()),
                    max=float(risk_values.max()),
                    min=float(risk_values.min())
                )
        
        # Recent items (up to 5, sorted by date descending)
        recent_items_list = []
        if title_col and title_col in day_df.columns:
            # Sort by date descending and take top 5
            day_df_sorted = day_df.sort_values('_date', ascending=False).head(5)
            
            for _, row in day_df_sorted.iterrows():
                title = str(row.get(title_col, "Untitled"))[:100]  # Truncate long titles
                department = str(row.get(dept_col, "Unknown")) if dept_col else "Unknown"
                date_val = row.get('_date')
                date_str = date_val.strftime('%Y-%m-%d') if pd.notna(date_val) else day_label
                severity_val = None
                if severity_col and severity_col in row.index:
                    sev = pd.to_numeric(row.get(severity_col), errors='coerce')
                    severity_val = float(sev) if pd.notna(sev) else None
                
                recent_items_list.append(RecentItem(
                    title=title,
                    department=department,
                    date=date_str,
                    severity=severity_val
                ))
        
        # Create day detail
        month_detail = MonthDetailedData(
            month=str(day_label),
            total_count=total_count,
            departments=departments_list,
            types=types_list,
            severity=severity_stats,
            risk=risk_stats,
            recent_items=recent_items_list
        )
        details.append(month_detail)
    
    # Build response
    response = DetailedTrendResponse(
        labels=counts.index.tolist(),
        series=[ChartSeries(name="Count", data=counts.values.astype(int).tolist())],
        details=details
    )
    
    return response


@router.get("/data/incident-type-distribution")
async def data_incident_type_distribution(
    dataset: str = Query("incident"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    min_severity: Optional[float] = Query(None, ge=0, le=5, description="Min severity"),
    max_severity: Optional[float] = Query(None, ge=0, le=5, description="Max severity"),
):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply flexible filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, min_severity=min_severity, max_severity=max_severity
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Include underscore variant to match documented column 'incident_type'
    type_col = _resolve_column(df, ["incident_type", "incident type(s)", "category", "accident type"]) or df.columns[0]
    vc = df[type_col].astype(str).str.split(",").explode().str.strip()
    counts = vc.value_counts().head(20)
    return JSONResponse(content={
        "labels": counts.index.tolist(),
        "series": [{"name": "Count", "data": counts.values.astype(int).tolist()}],
    })


@router.get("/data/root-cause-pareto/incident-types")
async def get_root_cause_incident_types(
    dataset: str = Query("incident"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
):
    """
    Get available incident types for the root cause pareto radio buttons.
    Respects current filters to show only relevant incident types.
    """
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, sublocations=sublocations, statuses=statuses
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"incident_types": []})
    
    # Get incident type column
    type_col = _resolve_column(df, ["incident_type(s)", "incident_type", "incident type(s)", "category"]) or df.columns[0]
    
    # Split and explode multi-value types
    types = df[type_col].dropna().astype(str).str.split(";").explode().str.strip()
    types = types[types != ""]
    types = types[~types.str.contains("nan|null|none|n/a", case=False, na=False, regex=True)]
    
    # Get unique types with counts
    type_counts = types.value_counts()
    
    # Return as list of objects with label and count
    incident_types = [
        {"label": "All", "value": "All", "count": len(df)}
    ] + [
        {"label": str(itype), "value": str(itype), "count": int(count)}
        for itype, count in type_counts.items()
    ]
    
    return JSONResponse(content={"incident_types": incident_types})


@router.get("/data/root-cause-pareto")
async def data_root_cause_pareto(
    dataset: str = Query("incident"),
    incident_type: Optional[str] = Query(None, description="Filter by specific incident type"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
    incident_types: Optional[List[str]] = Query(None, description="Filter by incident types"),
    top_n: int = Query(15, description="Number of top root causes to show"),
):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply standard filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, sublocations=sublocations, statuses=statuses,
        incident_types=incident_types
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "bars": [], "cum_pct": [], "incident_type": incident_type or "All"})
    
    # Additional filter by specific incident_type (radio button selection)
    if incident_type and incident_type.strip().lower() not in ["all", ""]:
        type_col = _resolve_column(df, ["incident_type(s)", "incident_type", "incident type(s)", "category"]) or df.columns[0]
        # Split multi-value incident types and filter
        df_exploded = df.copy()
        df_exploded["_type_split"] = df_exploded[type_col].astype(str).str.split(";")
        df_exploded = df_exploded.explode("_type_split")
        df_exploded["_type_split"] = df_exploded["_type_split"].str.strip()
        # Case-insensitive match
        mask = df_exploded["_type_split"].str.lower() == incident_type.strip().lower()
        df = df_exploded[mask].copy()
    
    if df.empty:
        return JSONResponse(content={"labels": [], "bars": [], "cum_pct": [], "incident_type": incident_type or "All"})
    
    # Extract and process root causes
    rc_col = _resolve_column(df, ["Root Cause", "root_cause", "root cause", "Key Factor", "key_factor", "Contributing Factor", "contributing_factor"]) or df.columns[0]
    
    # Split on semicolons and explode
    series = df[rc_col].dropna().astype(str)
    series = series.str.split(";").explode().str.strip()
    
    # Remove empty strings and placeholder values
    series = series[series != ""]
    series = series[~series.str.contains("nan|null|none|n/a|not applicable", case=False, na=False, regex=True)]
    
    if series.empty:
        return JSONResponse(content={"labels": [], "bars": [], "cum_pct": [], "incident_type": incident_type or "All"})
    
    # Count and get top N
    counts = series.value_counts()
    counts = counts.head(top_n)
    
    # Calculate cumulative percentage
    total = counts.sum() if counts.sum() > 0 else 1
    cum = counts.cumsum() / total * 100
    
    return JSONResponse(content={
        "labels": counts.index.tolist(),
        "bars": counts.values.astype(int).tolist(),
        "cum_pct": cum.round(2).values.tolist(),
        "incident_type": incident_type or "All",
        "total_count": int(counts.sum()),
    })


@router.get("/data/injury-severity-pyramid")
async def data_injury_severity_pyramid(dataset: str = Query("incident")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Support underscore and spaced variants
    sev_col = _resolve_column(
        df,
        [
            "injury_classification",
            "injury classification",
            "actual_consequence_incident",
            "actual consequence (incident)",
            "relevant_consequence_incident",
            "relevant consequence (incident)",
        ],
    ) or df.columns[0]
    order = ["Near Miss", "First Aid", "Recordable", "Lost Time", "Fatality"]
    vc = df[sev_col].astype(str).value_counts()
    labels = []
    data = []
    for o in order:
        if o in vc.index:
            labels.append(o)
            data.append(int(vc[o]))
    # append remaining categories
    for cat, val in vc.items():
        if cat not in labels:
            labels.append(str(cat))
            data.append(int(val))
    return JSONResponse(content={"labels": labels, "series": [{"name": "Count", "data": data}]})


@router.get("/data/department-month-heatmap")
async def data_department_month_heatmap(
    dataset: str = Query("incident"),
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    min_severity: Optional[float] = Query(None, ge=0, le=5, description="Min severity"),
    max_severity: Optional[float] = Query(None, ge=0, le=5, description="Max severity"),
    min_risk: Optional[float] = Query(None, ge=0, le=5, description="Min risk"),
    max_risk: Optional[float] = Query(None, ge=0, le=5, description="Max risk"),
):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    
    # Apply flexible filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, min_severity=min_severity, max_severity=max_severity,
        min_risk=min_risk, max_risk=max_risk
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"x": [], "y": [], "z": [], "metric": "count"})
    dep_col = _resolve_column(df, ["department"]) or _resolve_column(df, ["section"]) or df.columns[0]
    date_col = _resolve_column(df, ["occurrence_date", "date of occurrence", "date reported"]) or df.columns[0]
    months = _to_date_period(df[date_col], granularity='M')
    metric_col = _resolve_column(df, ["risk_score", "severity_score"])  # optional
    cp = pd.DataFrame({"department": df[dep_col].astype(str), "month": months})
    if metric_col is not None:
        cp["value"] = pd.to_numeric(df[metric_col], errors='coerce')
        pivot = cp.pivot_table(values="value", index="department", columns="month", aggfunc="mean")
        metric = "avg"
    else:
        cp["value"] = 1
        pivot = cp.pivot_table(values="value", index="department", columns="month", aggfunc="count")
        metric = "count"
    x = [str(c) for c in pivot.columns]
    y = [str(i) for i in pivot.index]
    z = pivot.fillna(0).to_numpy().tolist()
    return JSONResponse(content={"x": x, "y": y, "z": z, "metric": metric})


@router.get("/data/consequence-gap")
async def data_consequence_gap(dataset: str = Query("incident")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or df.empty:
        return JSONResponse(content={"rows": [], "cols": [], "z": []})
    # Support underscore and spaced variants
    actual = _resolve_column(df, ["actual_consequence_incident", "actual consequence (incident)"]) or df.columns[0]
    worst = _resolve_column(df, ["worst_case_consequence_incident", "worst case consequence (incident)"]) or df.columns[0]
    ct = pd.crosstab(df[actual], df[worst])
    return JSONResponse(content={
        "rows": [str(i) for i in ct.index],
        "cols": [str(c) for c in ct.columns],
        "z": ct.fillna(0).to_numpy().astype(int).tolist(),
    })


@router.get("/data/audit-status-distribution")
async def data_audit_status_distribution():
    df = get_audit_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Support both 'audit_status' and 'audit status'
    status_col = _resolve_column(df, ["audit_status", "audit status"]) or df.columns[0]
    vc = df[status_col].astype(str).value_counts()
    return JSONResponse(content={
        "labels": vc.index.tolist(),
        "series": [{"name": "Count", "data": vc.values.astype(int).tolist()}],
    })


@router.get("/data/audit-rating-trend")
async def data_audit_rating_trend():
    df = get_audit_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    date_col = _resolve_column(df, ["start_date", "start date"]) or df.columns[0]
    # Support both 'audit_rating' and 'audit rating'
    rating_col = _resolve_column(df, ["audit_rating", "audit rating"]) or None
    if rating_col is None:
        return JSONResponse(content={"labels": [], "series": []})
    months = _to_date_period(df[date_col], granularity='M')
    vals = pd.to_numeric(df[rating_col], errors='coerce')
    grp = pd.DataFrame({"month": months, "rating": vals}).groupby("month").mean().sort_index()
    return JSONResponse(content={
        "labels": grp.index.tolist(),
        "series": [{"name": "Avg Rating", "data": grp["rating"].round(2).fillna(0).tolist()}],
    })


@router.get("/data/audit-monthly-volume")
async def data_audit_monthly_volume(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
):
    """
    Monthly Audit Volume & Closures.

    - Deduplicates audits by ID
    - Initiated month = earliest Start Date (or Scheduled Date)
    - Closed month    = latest Entered Closed (or Completion/End Date)
    - Returns labels (YYYY-MM) and two series: Audits Initiated, Audits Closed
    """
    df = get_audit_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})

    # Apply filters early for consistency with other endpoints
    df = apply_analytics_filters(
        df,
        start_date=start_date,
        end_date=end_date,
        departments=departments,
        locations=locations,
        sublocations=sublocations,
        statuses=statuses,
    )
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})

    # Resolve columns (flexible matching across common variants)
    id_col = _resolve_column(df, [
        "audit number", "audit_number", "audit id", "audit_id",
    ])
    start_col = _resolve_column(df, [
        "start date", "start_date", "scheduled date", "scheduled_date",
    ])
    closed_col = _resolve_column(df, [
        "entered closed", "entered_closed", "completion date", "completion_date", "end date", "end_date",
    ])

    if id_col is None:
        # Create a surrogate ID if missing to avoid failure; use index
        df = df.copy()
        df["__audit_id_tmp"] = [f"AUD-{i+1}" for i in range(len(df))]
        id_col = "__audit_id_tmp"

    # Coerce date columns
    if start_col is not None:
        df[start_col] = pd.to_datetime(df[start_col], errors="coerce")
    if closed_col is not None:
        df[closed_col] = pd.to_datetime(df[closed_col], errors="coerce")

    # Deduplicate audits by ID, keeping earliest start and latest close
    agg_dict = {}
    if start_col is not None:
        agg_dict[start_col] = "min"
    if closed_col is not None:
        agg_dict[closed_col] = "max"
    if not agg_dict:
        return JSONResponse(content={"labels": [], "series": []})

    aud = df.groupby(id_col, as_index=False).agg(agg_dict)

    # Build initiated and closed month counts
    initiated = pd.Series(dtype=int)
    closed = pd.Series(dtype=int)

    if start_col is not None:
        aud["StartMonth"] = pd.to_datetime(aud[start_col], errors="coerce").dt.to_period("M")
        initiated = aud.dropna(subset=["StartMonth"]).groupby("StartMonth").size()
        initiated.name = "Audits Initiated"

    if closed_col is not None:
        aud["CloseMonth"] = pd.to_datetime(aud[closed_col], errors="coerce").dt.to_period("M")
        closed = aud.dropna(subset=["CloseMonth"]).groupby("CloseMonth").size()
        closed.name = "Audits Closed"

    # Merge into a unified monthly index
    if initiated.empty and closed.empty:
        return JSONResponse(content={"labels": [], "series": []})

    all_periods = sorted(set(initiated.index.tolist()) | set(closed.index.tolist()))
    if not all_periods:
        return JSONResponse(content={"labels": [], "series": []})

    # Ensure continuous range from min to max
    pmin = min(all_periods)
    pmax = max(all_periods)
    full_idx = pd.period_range(pmin, pmax, freq="M")

    monthly = pd.DataFrame(index=full_idx)
    if not initiated.empty:
        monthly["Audits Initiated"] = initiated
    if not closed.empty:
        monthly["Audits Closed"] = closed

    monthly = monthly.fillna(0).astype(int)

    labels = [str(p) for p in monthly.index]
    series = []
    if "Audits Initiated" in monthly.columns:
        series.append({"name": "Audits Initiated", "data": monthly["Audits Initiated"].tolist()})
    if "Audits Closed" in monthly.columns:
        series.append({"name": "Audits Closed", "data": monthly["Audits Closed"].tolist()})

    return JSONResponse(content={"labels": labels, "series": series})


@router.get("/data/inspection-coverage")
async def data_inspection_coverage():
    df = get_inspection_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    date_col = _resolve_column(df, ["start_date", "start date"]) or df.columns[0]
    # Support both 'audit_status' and 'audit status'
    status_col = _resolve_column(df, ["audit_status", "audit status"]) or df.columns[0]
    months = _to_date_period(df[date_col], granularity='M')
    tmp = pd.DataFrame({"month": months, "status": df[status_col].astype(str)})
    pivot = tmp.pivot_table(index="month", columns="status", values="status", aggfunc="count").fillna(0).astype(int)
    pivot = pivot.sort_index()
    labels = pivot.index.tolist()
    series = [{"name": str(col), "data": pivot[col].tolist()} for col in pivot.columns]
    return JSONResponse(content={"labels": labels, "series": series})


@router.get("/data/inspection-top-findings")
async def data_inspection_top_findings(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
):
    df = get_inspection_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Apply filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, sublocations=sublocations, statuses=statuses
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Prefer granular finding/observation text; fallback to checklist category
    col_candidates = [
        "finding", "findings", "observation", "observations", "non_conformance", "non conformance",
        "issue", "issues", "remark", "remarks", "description",
        "checklist_category", "checklist category"
    ]
    col = _resolve_column(df, col_candidates) or df.columns[0]

    series = df[col].dropna().astype(str)

    # Normalize whitespace and strip punctuation
    series = series.str.replace(r"\s+", " ", regex=True).str.strip(" \t\r\n-–•·;:,.")

    # Remove placeholders and generic negations
    na_pat = re.compile(r"^(n/?a|na|nan|null|none|not\s*applicable)$", re.IGNORECASE)
    no_pat = re.compile(r"^no(\s+|$)|no\s+(finding|findings|observation|observations|deficien(?:cy|cies)|issue|issues|recommendation(?:s)?)$", re.IGNORECASE)
    mask = (~series.str.match(na_pat)) & (~series.str.match(no_pat)) & (series.str.len() > 0)
    series = series[mask]

    # If we are using a category-like column, split on delimiters and explode to avoid concatenated labels
    is_category_like = col.lower().strip() in {"checklist_category", "checklist category"}
    if is_category_like:
        # Split on ';' or ',' and explode
        series = series.str.split(r"[;,]").explode().astype(str)
        # Re-normalize tokens
        series = series.str.replace(r"\s+", " ", regex=True).str.strip(" \t\r\n-–•·;:,.")
        # Drop empty after split
        series = series[series.str.len() > 0]

    # Canonicalize casing for consistent aggregation
    tokens = series.str.strip().str.replace(r"\s+", " ", regex=True)

    # Build value counts and take top 20
    vc = tokens.value_counts().head(20)
    labels = [str(x) for x in vc.index.tolist()]
    counts = vc.values.astype(int).tolist()

    return JSONResponse(content={
        "labels": labels,
        "series": [{"name": "Count", "data": counts}],
    })


@router.get("/data/audit-top-findings")
async def data_audit_top_findings(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
):
    df = get_audit_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Apply filters
    df = apply_analytics_filters(
        df, start_date=start_date, end_date=end_date, departments=departments,
        locations=locations, sublocations=sublocations, statuses=statuses
    )
    
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Prefer granular finding/observation text; fallback to checklist category
    col_candidates = [
        "finding", "findings", "observation", "observations", "non_conformance", "non conformance",
        "issue", "issues", "remark", "remarks", "description",
        "checklist_category", "checklist category"
    ]
    col = _resolve_column(df, col_candidates) or df.columns[0]

    series = df[col].dropna().astype(str)

    # Normalize whitespace and strip punctuation
    series = series.str.replace(r"\s+", " ", regex=True).str.strip(" \t\r\n-–•·;:,.")

    # Remove placeholders and generic negations
    na_pat = re.compile(r"^(n/?a|na|nan|null|none|not\s*applicable)$", re.IGNORECASE)
    no_pat = re.compile(r"^no(\s+|$)|no\s+(finding|findings|observation|observations|deficien(?:cy|cies)|issue|issues|recommendation(?:s)?)$", re.IGNORECASE)
    mask = (~series.str.match(na_pat)) & (~series.str.match(no_pat)) & (series.str.len() > 0)
    series = series[mask]

    # If we are using a category-like column, split on delimiters and explode to avoid concatenated labels
    is_category_like = col.lower().strip() in {"checklist_category", "checklist category"}
    if is_category_like:
        # Split on ';' or ',' and explode
        series = series.str.split(r"[;,]").explode().astype(str)
        # Re-normalize tokens
        series = series.str.replace(r"\s+", " ", regex=True).str.strip(" \t\r\n-–•·;:,.")
        # Drop empty after split
        series = series[series.str.len() > 0]

    # Canonicalize casing for consistent aggregation
    tokens = series.str.strip().str.replace(r"\s+", " ", regex=True)

    # Build value counts and take top 20
    vc = tokens.value_counts().head(20)
    labels = [str(x) for x in vc.index.tolist()]
    counts = vc.values.astype(int).tolist()

    return JSONResponse(content={
        "labels": labels,
        "series": [{"name": "Count", "data": counts}],
    })


@router.get("/data/incident-top-findings")
async def data_incident_top_findings(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
    violation_types: Optional[List[str]] = Query(None, description="Filter by violation types"),
    min_count: int = Query(8, description="Minimum count to avoid grouping as 'Others'"),
):
    """
    Returns hazards grouped by Incident Type with severity breakdown from Hazard ID sheet.
    Creates a stacked bar chart showing severity distribution per incident type.
    Uses: Sheet='Hazard ID', Columns=['Incident Type(s)', 'Worst Case Consequence Potential (Hazard ID)']
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
    
    # Helper function to clean text
    def clean_column(series):
        return (
            series.astype(str)
            .str.replace("\xa0", " ", regex=False)
            .str.replace(r"\s+", " ", regex=True)
            .str.strip()
            .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA, "null": pd.NA, "NULL": pd.NA})
        )
    
    # Find incident type column
    incident_col_candidates = [
        "incident_type(s)", "incident type(s)", "incident_types", "incident type", "incident_type"
    ]
    incident_col = _resolve_column(df, incident_col_candidates)
    
    # Find severity column - Use Hazard ID severity column as specified
    severity_col_candidates = [
        "worst case consequence potential (hazard id)",
        "worst_case_consequence_potential_hazard_id",
        "worst case consequence potential hazard id",
        "worst_case_consequence_potential_(hazard_id)"
    ]
    severity_col = _resolve_column(df, severity_col_candidates)
    
    if incident_col is None or severity_col is None:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Clean both columns
    df[incident_col] = clean_column(df[incident_col])
    df[severity_col] = clean_column(df[severity_col])
    
    # Drop rows with NA in either column
    df_clean = df.dropna(subset=[incident_col, severity_col])
    
    if df_clean.empty:
        return JSONResponse(content={"labels": [], "series": []})
    
    # Group small incident types into "Others"
    counts = df_clean[incident_col].value_counts()
    main_incidents = counts[counts >= min_count].index
    
    df_filtered = df_clean[df_clean[incident_col].isin(main_incidents)].copy()
    
    # Add "Others" group
    if (counts < min_count).any():
        others_df = df_clean[~df_clean[incident_col].isin(main_incidents)].copy()
        if not others_df.empty:
            others_df[incident_col] = "Others"
            df_filtered = pd.concat([df_filtered, others_df], ignore_index=True)
    
    # Define severity order (only C0-C3 for Hazard ID sheet as specified)
    severity_order = ["C0 - No Ill Effect", "C1 - Minor", "C2 - Serious", "C3 - Severe"]
    
    # Create crosstab
    matrix = pd.crosstab(df_filtered[incident_col], df_filtered[severity_col])
    
    # Ensure all severity levels exist
    for sev in severity_order:
        if sev not in matrix.columns:
            matrix[sev] = 0
    
    # Order columns and sort rows by total
    matrix = matrix[severity_order]
    matrix["Total"] = matrix.sum(axis=1)
    matrix = matrix.sort_values("Total", ascending=False)
    totals = matrix["Total"].astype(int).tolist()
    matrix = matrix.drop(columns="Total")
    
    # Build response
    labels = matrix.index.tolist()  # Incident types (x-axis)
    series = [
        {"name": sev, "data": matrix[sev].astype(int).tolist()}
        for sev in severity_order
    ]
    
    return JSONResponse(content={
        "labels": labels,
        "series": series,
        "totals": totals,
        "legend": severity_order,
        "records_used": int(df_clean.shape[0]),
        "min_count_for_others": int(min_count)
    })


@router.get("/data/hazard-top-findings")
async def data_hazard_top_findings(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    departments: Optional[List[str]] = Query(None, description="Filter by departments"),
    locations: Optional[List[str]] = Query(None, description="Filter by locations"),
    sublocations: Optional[List[str]] = Query(None, description="Filter by sublocations"),
    statuses: Optional[List[str]] = Query(None, description="Filter by status"),
    violation_types: Optional[List[str]] = Query(None, description="Filter by violation types"),
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
    
    # Look for 'Incident Type(s)' column (with or without parentheses/spaces)
    col_candidates = [
        "incident_type(s)",
        "incident type(s)",
        "incident_types",
        "incident type",
        "incident_type"
    ]
    col = _resolve_column(df, col_candidates)
    
    if col is None:
        # Fallback to empty result if column not found
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
    
    # Return all categories (no limit, to match your pattern)
    labels = [str(x) for x in vc.index.tolist()]
    counts = vc.values.astype(int).tolist()
    
    return JSONResponse(content={
        "labels": labels,
        "series": [{"name": "Hazards", "data": counts}],
    })


@router.get("/data/incident-cost-trend")
async def data_incident_cost_trend(dataset: str = Query("incident")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    date_col = _resolve_column(df, ["occurrence_date", "date of occurrence", "date reported"]) or df.columns[0]
    cost_col = _resolve_column(df, ["total cost", "estimated_cost_impact"]) or None
    if cost_col is None:
        return JSONResponse(content={"labels": [], "series": []})
    months = _to_date_period(df[date_col], granularity='M')
    vals = pd.to_numeric(df[cost_col], errors='coerce')
    grp = pd.DataFrame({"month": months, "cost": vals}).groupby("month").sum().sort_index()
    return JSONResponse(content={
        "labels": grp.index.tolist(),
        "series": [{"name": "Total Cost", "data": grp["cost"].round(0).fillna(0).astype(float).tolist()}],
    })


@router.get("/data/hazard-cost-trend")
async def data_hazard_cost_trend():
    return await data_incident_cost_trend(dataset="hazard")


@router.get("/data/repeated-incidents")
async def data_repeated_incidents():
    df = get_incident_df()
    if df is None or df.empty:
        return JSONResponse(content={"labels": [], "series": []})
    # Support underscore and spaced variants
    rep_col = _resolve_column(df, ["repeated_incident", "repeated incident", "repeated_event", "repeated event"]) or None
    loc_col = _resolve_column(
        df,
        [
            "specific_location_of_occurrence",
            "specific location of occurrence",
            "sub_location",
            "sub-location",
            "sublocation",
            "location",
        ],
    ) or None
    if rep_col is None or loc_col is None:
        return JSONResponse(content={"labels": [], "series": []})
    mask = df[rep_col].astype(str).str.lower().isin(["yes", "true", "1"])
    vc = df.loc[mask, loc_col].astype(str).value_counts().head(15)
    return JSONResponse(content={
        "labels": vc.index.tolist(),
        "series": [{"name": "Repeated Count", "data": vc.values.astype(int).tolist()}],
    })

@router.get("/hse-scorecard/insights", response_model=ChartInsightsResponse)
async def hse_scorecard_insights():
    title = "Unified HSE Scorecard"
    inc = get_incident_df()
    haz = get_hazard_df()
    aud = get_audit_df()
    ins = get_inspection_df()
    inc_count = len(inc) if isinstance(inc, pd.DataFrame) else 0
    haz_count = len(haz) if isinstance(haz, pd.DataFrame) else 0
    audits_completed = 0
    if isinstance(aud, pd.DataFrame) and 'audit_status' in aud.columns:
        audits_completed = (aud['audit_status'].astype(str).str.lower() == 'closed').sum()
    insp_count = len(ins) if isinstance(ins, pd.DataFrame) else 0
    summary = {
        'title': title,
        'kpis': {
            'incidents': inc_count,
            'hazards': haz_count,
            'audits_completed': int(audits_completed),
            'inspections': insp_count,
        }
    }
    try:
        prompt = (
            "Provide concise markdown insights for the HSE scorecard KPIs (incidents, hazards, audits completed, inspections). "
            "Highlight notable imbalances, trends to watch, and 3-4 short recommendations."
        )
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    parts.append(f"- **Incidents**: {inc_count}")
    parts.append(f"- **Hazards**: {haz_count}")
    parts.append(f"- **Audits completed**: {audits_completed}")
    parts.append(f"- **Inspections**: {insp_count}")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Set monthly targets for incident/hazard reduction.")
    parts.append("- **Action**: Ensure timely closure of audits and follow-ups.")
    parts.append("- **Action**: Maintain inspection cadence in high-risk areas.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/hse-performance-index", response_model=PlotlyFigureResponse)
async def hse_performance_index(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_hse_performance_index(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/hse-performance-index/insights", response_model=ChartInsightsResponse)
async def hse_performance_index_insights(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    # Data-driven HSE index computation from dataset
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    title = "HSE Performance Index"
    if df is None or df.empty or 'department' not in df.columns:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    cp = df.copy()
    # Coerce relevant columns
    for c in ['severity_score', 'risk_score', 'reporting_delay_days', 'resolution_time_days', 'root_cause_is_missing', 'corrective_actions_is_missing']:
        if c not in cp.columns:
            cp[c] = np.nan
    def _to_days(series: pd.Series) -> pd.Series:
        try:
            if series is None:
                return series
            s = series
            if np.issubdtype(s.dtype, np.timedelta64):
                return s.dt.total_seconds() / 86400.0
            if np.issubdtype(s.dtype, np.datetime64):
                return pd.to_numeric(s, errors='coerce')
            return pd.to_numeric(s, errors='coerce')
        except Exception:
            return pd.to_numeric(series, errors='coerce')
    cp['reporting_delay_days'] = _to_days(cp['reporting_delay_days'])
    cp['resolution_time_days'] = _to_days(cp['resolution_time_days'])
    for c in ['severity_score', 'risk_score']:
        cp[c] = pd.to_numeric(cp[c], errors='coerce')
    for c in ['root_cause_is_missing', 'corrective_actions_is_missing']:
        cp[c] = pd.to_numeric(cp[c].astype(float), errors='coerce')
    dept_metrics = cp.groupby('department').agg({
        'severity_score': 'mean',
        'risk_score': 'mean',
        'reporting_delay_days': 'mean',
        'resolution_time_days': 'mean',
        'root_cause_is_missing': 'mean',
        'corrective_actions_is_missing': 'mean'
    }).fillna(0)
    sev = dept_metrics['severity_score'].clip(lower=0, upper=5)
    risk = dept_metrics['risk_score'].clip(lower=0, upper=5)
    rep = dept_metrics['reporting_delay_days'].clip(lower=0, upper=30)
    res = dept_metrics['resolution_time_days'].clip(lower=0, upper=60)
    rc_miss = dept_metrics['root_cause_is_missing'].clip(lower=0, upper=1)
    ca_miss = dept_metrics['corrective_actions_is_missing'].clip(lower=0, upper=1)
    idx = ((5 - sev)/5 * 0.25 + (5 - risk)/5 * 0.25 + (30 - rep)/30 * 0.2 + (60 - res)/60 * 0.2 + (1 - rc_miss) * 0.05 + (1 - ca_miss) * 0.05) * 100
    scores = idx.sort_values(ascending=False)
    summary = {
        'title': title,
        'scores': [{ 'department': str(k), 'index': float(v) } for k, v in scores.items()],
        'top5': [{ 'department': str(k), 'index': float(v)} for k, v in scores.head(5).items()],
        'bottom5': [{ 'department': str(k), 'index': float(v)} for k, v in scores.tail(5).items()],
        'components': {
            'severity_score_mean': { str(k): float(v) for k, v in sev.items() },
            'risk_score_mean': { str(k): float(v) for k, v in risk.items() },
            'reporting_delay_days_mean': { str(k): float(v) for k, v in rep.items() },
            'resolution_time_days_mean': { str(k): float(v) for k, v in res.items() },
        }
    }
    try:
        prompt = (
            "Using the HSE index per department (0-100), write concise markdown insights: top/bottom performers, "
            "what drives high/low scores (severity, risk, delays), and 3-4 recommendations."
        )
        llm_md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if llm_md and not llm_md.lower().startswith("openai") and "not installed" not in llm_md.lower():
            return ChartInsightsResponse(insights_md=llm_md)
    except Exception:
        pass
    # Fallback
    parts = [f"## {title}"]
    if len(scores) > 0:
        parts.append(f"- **Top**: {scores.index[0]} ({scores.iloc[0]:.1f})")
        parts.append(f"- **Bottom**: {scores.index[-1]} ({scores.iloc[-1]:.1f})")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Target low-scoring departments with focused interventions on severity/risk reduction.")
    parts.append("- **Action**: Reduce reporting and resolution delays where averages are highest.")
    parts.append("- **Action**: Share practices from top performers to lift underperformers.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/psm-breakdown", response_model=PlotlyFigureResponse)
async def psm_breakdown(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_psm_breakdown(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/psm-breakdown/insights", response_model=ChartInsightsResponse)
async def psm_breakdown_insights(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    # Data-driven PSM breakdown
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    title = "Process Safety Management Analysis"
    if df is None or df.empty:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    psm_counts = df['psm'].value_counts(dropna=True) if 'psm' in df.columns else pd.Series(dtype=int)
    pse_counts = df['pse_category'].value_counts(dropna=True) if 'pse_category' in df.columns else pd.Series(dtype=int)
    summary = {
        'title': title,
        'psm_top': [{ 'label': str(k), 'count': int(v)} for k, v in psm_counts.head(10).items()],
        'pse_top': [{ 'label': str(k), 'count': int(v)} for k, v in pse_counts.head(10).items()],
        'total': int(len(df)),
    }
    try:
        prompt = (
            "Summarize PSM and PSE distributions: top elements/categories and where to focus. Provide concise markdown with recommendations."
        )
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if not psm_counts.empty:
        k, v = next(iter(psm_counts.items()))
        parts.append(f"- **Top PSM element**: {k} ({v})")
    if not pse_counts.empty:
        k, v = next(iter(pse_counts.items()))
        parts.append(f"- **Top PSE category**: {k} ({v})")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Prioritize top categories for deeper root-cause analysis.")
    parts.append("- **Action**: Track monthly shifts in leading categories.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/data-quality-metrics", response_model=PlotlyFigureResponse)
async def data_quality_metrics(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_data_quality_metrics(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/data-quality-metrics/insights", response_model=ChartInsightsResponse)
async def data_quality_metrics_insights(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    title = "Data Quality Metrics"
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or df.empty:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    cp = df.copy()
    rc_col = 'root_cause_is_missing'
    ca_col = 'corrective_actions_is_missing'
    rep_col = 'reporting_delay_days'
    res_col = 'resolution_time_days'
    for c in [rc_col, ca_col]:
        if c in cp.columns:
            cp[c] = pd.to_numeric(cp[c].astype(float), errors='coerce')
    rep = pd.to_numeric(cp.get(rep_col, pd.Series(dtype=float)), errors='coerce') if rep_col in cp.columns else pd.Series(dtype=float)
    res = pd.to_numeric(cp.get(res_col, pd.Series(dtype=float)), errors='coerce') if res_col in cp.columns else pd.Series(dtype=float)
    status = cp['status'].astype(str) if 'status' in cp.columns else pd.Series(dtype=str)
    summary = {
        'title': title,
        'missing_root_cause_rate': float(cp[rc_col].mean()) if rc_col in cp.columns and len(cp) else None,
        'missing_actions_rate': float(cp[ca_col].mean()) if ca_col in cp.columns and len(cp) else None,
        'reporting_delay_mean': float(rep.mean()) if rep.notna().any() else None,
        'reporting_delay_p95': float(rep.quantile(0.95)) if rep.notna().any() else None,
        'resolution_time_mean': float(res.mean()) if res.notna().any() else None,
        'resolution_time_p95': float(res.quantile(0.95)) if res.notna().any() else None,
        'resolution_by_status': status.value_counts().head(10).to_dict() if not status.empty else {},
    }
    try:
        prompt = "Provide concise markdown on data quality: missing fields, delays, resolution by status, and actions to improve data capture."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if summary['missing_root_cause_rate'] is not None:
        parts.append(f"- **Root cause missing**: {summary['missing_root_cause_rate']*100:.0f}%")
    if summary['missing_actions_rate'] is not None:
        parts.append(f"- **Actions missing**: {summary['missing_actions_rate']*100:.0f}%")
    if summary['reporting_delay_mean'] is not None:
        parts.append(f"- **Reporting delay (mean/p95)**: {summary['reporting_delay_mean']:.1f} / {summary['reporting_delay_p95']:.1f} days")
    if summary['resolution_time_mean'] is not None:
        parts.append(f"- **Resolution time (mean/p95)**: {summary['resolution_time_mean']:.1f} / {summary['resolution_time_p95']:.1f} days")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Improve mandatory capture of root cause and actions.")
    parts.append("- **Action**: Triage records exceeding 95th percentile delays.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/audit-inspection-tracker", response_model=PlotlyFigureResponse)
async def audit_inspection_tracker():
    audit_df = get_audit_df()
    inspection_df = get_inspection_df()
    fig = plot_service.create_audit_inspection_tracker(audit_df, inspection_df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/audit-inspection-tracker/insights", response_model=ChartInsightsResponse)
async def audit_inspection_traker_insights():
    title = "Audit & Inspection Compliance Tracking"
    audit_df = get_audit_df()
    inspection_df = get_inspection_df()
    def _timeline(df: pd.DataFrame):
        if df is None or not {'start_date','audit_status'}.issubset(df.columns):
            return None
        d = df.copy()
        d['_m'] = pd.to_datetime(d['start_date'], errors='coerce').dt.to_period('M')
        totals = d.groupby('_m').size()
        by_status = d.groupby([d['_m'], 'audit_status']).size().unstack(fill_value=0)
        return {
            'months': [str(ix) for ix in totals.index],
            'totals': [int(v) for v in totals.values],
            'by_status': { str(k): [int(x) for x in by_status[k].values] for k in by_status.columns }
        }
    aud = _timeline(audit_df)
    ins = _timeline(inspection_df)
    summary = { 'title': title, 'audit': aud, 'inspection': ins }
    try:
        prompt = "Summarize audits and inspections over time: totals trend, dominant statuses, and actions to improve throughput."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if aud and aud['totals']:
        parts.append(f"- **Audits — last month total**: {aud['totals'][-1]}")
    if ins and ins['totals']:
        parts.append(f"- **Inspections — last month total**: {ins['totals'][-1]}")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Address bottleneck statuses with SLAs.")
    parts.append("- **Action**: Balance workload across months to avoid spikes.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/location-risk-treemap", response_model=PlotlyFigureResponse)
async def location_risk_treemap(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_location_risk_treemap(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/location-risk-treemap/insights", response_model=ChartInsightsResponse)
async def location_risk_treemap_insights(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    title = "Location Risk Map"
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or not {'location','sublocation'}.issubset(df.columns):
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    cp = df.copy()
    for c in ['severity_score','risk_score','estimated_cost_impact']:
        if c in cp.columns:
            cp[c] = pd.to_numeric(cp[c], errors='coerce')
    g = cp.groupby(['location','sublocation']).agg(
        count=('sublocation','count'),
        avg_severity=('severity_score','mean'),
        avg_risk=('risk_score','mean'),
        total_cost=('estimated_cost_impact','sum')
    ).fillna(0).reset_index()
    top_count = g.sort_values('count', ascending=False).head(5)
    top_risk = g.sort_values('avg_risk', ascending=False).head(5)
    summary = {
        'title': title,
        'top_hotspots_by_count': g.sort_values('count', ascending=False).head(10).to_dict(orient='records'),
        'top_hotspots_by_risk': g.sort_values('avg_risk', ascending=False).head(10).to_dict(orient='records'),
    }
    try:
        prompt = "Summarize location hotspots by count and by risk; include 3-4 actions to mitigate hotspots."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if not top_count.empty:
        r0 = top_count.iloc[0]
        parts.append(f"- **Most incidents**: {r0['location']} / {r0['sublocation']} ({int(r0['count'])})")
    if not top_risk.empty:
        r1 = top_risk.iloc[0]
        parts.append(f"- **Highest risk**: {r1['location']} / {r1['sublocation']} (avg {r1['avg_risk']:.2f})")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Audit top hotspots for immediate controls.")
    parts.append("- **Action**: Increase monitoring in high-risk sublocations.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/violation-analysis", response_model=PlotlyFigureResponse)
async def violation_analysis(dataset: str = Query("hazard", description="Dataset to use: incident or hazard")):
    df = get_hazard_df() if (dataset or "hazard").lower() == "hazard" else get_incident_df()
    fig = plot_service.create_violation_analysis(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/violation-analysis/insights", response_model=ChartInsightsResponse)
async def violation_analysis_insights(dataset: str = Query("hazard", description="Dataset to use: incident or hazard")):
    title = "Hazard Violation Analysis"
    df = get_hazard_df() if (dataset or "hazard").lower() == "hazard" else get_incident_df()
    if df is None:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    summary = {'title': title}
    if 'violation_type_hazard_id' in df.columns:
        vc = df['violation_type_hazard_id'].value_counts().head(10)
        summary['violation_types_top'] = vc.to_dict()
    if 'worst_case_consequence_potential_hazard_id' in df.columns:
        wc = df['worst_case_consequence_potential_hazard_id'].value_counts().head(10)
        summary['worst_case_top'] = wc.to_dict()
    if 'reporting_delay_days' in df.columns:
        rd = pd.to_numeric(df['reporting_delay_days'], errors='coerce')
        summary['reporting_delay_mean'] = float(rd.mean()) if rd.notna().any() else None
        summary['reporting_delay_p95'] = float(rd.quantile(0.95)) if rd.notna().any() else None
    if {'department','violation_type_hazard_id'}.issubset(df.columns):
        heat = df.pivot_table(index='department', columns='violation_type_hazard_id', values='violation_type_hazard_id', aggfunc='count').fillna(0)
        # Top department-violation pairs
        pairs = []
        for i, dep in enumerate(heat.index):
            for j, vt in enumerate(heat.columns):
                val = float(heat.iloc[i, j])
                if val > 0:
                    pairs.append({'department': str(dep), 'violation_type': str(vt), 'count': int(val)})
        summary['top_pairs'] = sorted(pairs, key=lambda x: x['count'], reverse=True)[:10]
    try:
        prompt = "Summarize violation distributions and highlight top department-violation pairs with actions."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if 'violation_types_top' in summary and summary['violation_types_top']:
        top_k, top_v = next(iter(summary['violation_types_top'].items()))
        parts.append(f"- **Most common violation**: {top_k} ({top_v})")
    if 'worst_case_top' in summary and summary['worst_case_top']:
        wk, wv = next(iter(summary['worst_case_top'].items()))
        parts.append(f"- **Top worst-case category**: {wk} ({wv})")
    if summary.get('reporting_delay_mean') is not None:
        parts.append(f"- **Reporting delay (mean/p95)**: {summary['reporting_delay_mean']:.1f} / {summary['reporting_delay_p95']:.1f} days")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Target most common violations with training and controls.")
    parts.append("- **Action**: Engage departments with highest violation pairs.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/cost-prediction-analysis", response_model=PlotlyFigureResponse)
async def cost_prediction_analysis(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_cost_prediction_analysis(df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/cost-prediction-analysis/insights", response_model=ChartInsightsResponse)
async def cost_prediction_analysis_insights(dataset: str = Query("incident", description="Dataset to use: incident or hazard")):
    title = "Cost Impact Analysis"
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    if df is None or 'estimated_cost_impact' not in df.columns:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    sub_cols = [c for c in ['severity_score','risk_score','reporting_delay_days','resolution_time_days','estimated_manhours_impact'] if c in df.columns]
    sub = df[sub_cols + ['estimated_cost_impact']].copy() if sub_cols else pd.DataFrame()
    for c in sub.columns:
        sub[c] = pd.to_numeric(sub[c], errors='coerce')
    corrs = {}
    if not sub.empty and len(sub_cols) > 0:
        cor = sub.corr(numeric_only=True)['estimated_cost_impact'].drop('estimated_cost_impact', errors='ignore')
        corrs = { str(k): float(v) for k, v in cor.items() } if cor is not None else {}
    summary = {
        'title': title,
        'top_correlations': sorted(corrs.items(), key=lambda x: abs(x[1]), reverse=True),
        'cost_stats': {
            'mean': float(pd.to_numeric(df['estimated_cost_impact'], errors='coerce').mean()),
            'p95': float(pd.to_numeric(df['estimated_cost_impact'], errors='coerce').quantile(0.95)),
        }
    }
    try:
        prompt = "Summarize key drivers of cost (correlations) and provide actions to reduce cost outliers."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if summary['top_correlations']:
        k, v = summary['top_correlations'][0]
        parts.append(f"- **Strongest correlation with cost**: {k} ({v:+.2f})")
    parts.append(f"- **Cost (mean/p95)**: {summary['cost_stats']['mean']:.0f} / {summary['cost_stats']['p95']:.0f}")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Address drivers with strongest positive correlation.")
    parts.append("- **Action**: Review processes for top 5% most expensive incidents.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/facility-layout-heatmap", response_model=PlotlyFigureResponse)
async def facility_layout_heatmap():
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    fig = plot_service.create_facility_layout_heatmap(inc_df, haz_df)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/facility-layout-heatmap/insights", response_model=ChartInsightsResponse)
async def facility_layout_heatmap_insights():
    title = "Facility Risk Heat Map"
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    def _zone_summary(df: pd.DataFrame, label: str):
        if df is None or df.empty:
            return None
        zones = getattr(plot_service, 'FACILITY_ZONES', {})
        rows = []
        for zone_name, info in zones.items():
            count = 0
            sev_sum = 0.0
            risk_sum = 0.0
            for col in ['location.1','sublocation','location']:
                if col in df.columns:
                    m = df[df[col].astype(str).str.contains(zone_name, case=False, na=False)]
                    count += len(m)
                    if 'severity_score' in df.columns:
                        sev_sum += pd.to_numeric(m['severity_score'], errors='coerce').fillna(0).sum()
                    if 'risk_score' in df.columns:
                        risk_sum += pd.to_numeric(m['risk_score'], errors='coerce').fillna(0).sum()
            avg_sev = (sev_sum / count) if count > 0 else 0.0
            avg_risk = (risk_sum / count) if count > 0 else 0.0
            rows.append({'zone': zone_name, 'area': info.get('area'), 'count': int(count), 'avg_severity': float(avg_sev), 'avg_risk': float(avg_risk)})
        rows = [r for r in rows if r['count'] > 0]
        rows.sort(key=lambda r: r['count'], reverse=True)
        return {'label': label, 'top_by_count': rows[:5], 'top_by_risk': sorted(rows, key=lambda r: r['avg_risk'], reverse=True)[:5]}
    inc = _zone_summary(inc_df, 'Incidents')
    haz = _zone_summary(haz_df, 'Hazards')
    summary = {'title': title, 'incidents': inc, 'hazards': haz}
    try:
        prompt = "Summarize top facility zones by incidents and risk for incidents and hazards; include actions."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if inc and inc['top_by_count']:
        r = inc['top_by_count'][0]
        parts.append(f"- **Incidents hotspot**: {r['zone']} ({r['count']})")
    if haz and haz['top_by_count']:
        r = haz['top_by_count'][0]
        parts.append(f"- **Hazards hotspot**: {r['zone']} ({r['count']})")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Conduct targeted inspections in hotspot zones.")
    parts.append("- **Action**: Strengthen controls in high-risk areas.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.get("/facility-3d-heatmap", response_model=PlotlyFigureResponse)
async def facility_3d_heatmap(
    dataset: str = Query("incident", description="Dataset to use: incident or hazard"),
    event_type: str = Query("Incidents", description="Label for the 3D surface legend/title"),
):
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    fig = plot_service.create_3d_facility_heatmap(df, event_type=event_type)
    return JSONResponse(content={"figure": to_native_json(fig.to_plotly_json())})


@router.get("/facility-3d-heatmap/insights", response_model=ChartInsightsResponse)
async def facility_3d_heatmap_insights(
    dataset: str = Query("incident", description="Dataset to use: incident or hazard"),
    event_type: str = Query("Incidents", description="Label for the 3D surface legend/title"),
):
    title = f"3D {event_type} Heat Map"
    df = get_incident_df() if (dataset or "incident").lower() == "incident" else get_hazard_df()
    # Provide zone-based summary similar to 2D layout
    if df is None or df.empty:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: Not enough data to analyze.")
    zones = getattr(plot_service, 'FACILITY_ZONES', {})
    rows = []
    for zone_name, _ in zones.items():
        count = 0
        sev_sum = 0.0
        for col in ['location.1','sublocation','location']:
            if col in df.columns:
                m = df[df[col].astype(str).str.contains(zone_name, case=False, na=False)]
                count += len(m)
                if 'severity_score' in df.columns:
                    sev_sum += pd.to_numeric(m['severity_score'], errors='coerce').fillna(0).sum()
        avg_sev = (sev_sum / count) if count > 0 else 0.0
        rows.append({'zone': zone_name, 'count': int(count), 'avg_severity': float(avg_sev)})
    rows = [r for r in rows if r['count'] > 0]
    top_count = sorted(rows, key=lambda r: r['count'], reverse=True)[:5]
    summary = {'title': title, 'event_type': event_type, 'top_zones': top_count}
    try:
        prompt = "Summarize 3D heat map hotspots (zones with highest counts/severity) with actions."
        md = ask_openai(prompt, context=json.dumps(summary, ensure_ascii=False), model="gpt-4o", code_mode=False, multi_df=False)
        if md and not md.lower().startswith("openai") and "not installed" not in md.lower():
            return ChartInsightsResponse(insights_md=md)
    except Exception:
        pass
    parts = [f"## {title}"]
    if top_count:
        r = top_count[0]
        parts.append(f"- **Top zone**: {r['zone']} ({r['count']}) — avg severity {r['avg_severity']:.2f}")
    parts.append("\n### Recommendations")
    parts.append("- **Action**: Prioritize mitigation in highest-intensity 3D zones.")
    parts.append("- **Action**: Compare with 2D layout hotspots for consistency.")
    return ChartInsightsResponse(insights_md="\n".join(parts))


@router.post("/insights", response_model=ChartInsightsResponse)
async def generate_chart_insights(payload: ChartInsightsRequest) -> ChartInsightsResponse:
    """Generate layman-friendly insights from a Plotly figure JSON.
    Heuristic summary first, then optionally refined with LLM if available.
    """
    fig = payload.figure or {}
    title = (
        payload.title
        or ((fig.get("layout", {}) or {}).get("title", {}) or {}).get("text")
        or (fig.get("layout", {}) or {}).get("title")
        or "Chart"
    )

    # Prefer OpenAI-based generator for insights; fallback to heuristic if it fails
    try:
        generator = PlotlyInsightsGenerator()
        extracted = generator.extractor.extract_all_data(fig)
        insight_types = [InsightType.EXECUTIVE_SUMMARY]
        if len(extracted.get("traces", [])) > 1:
            insight_types.append(InsightType.TRENDS)
        if any(((t.get("statistics", {}) or {}).get("std", 0) not in (None, 0)) for t in extracted.get("traces", [])):
            insight_types.append(InsightType.ANOMALIES)
        insight_types.append(InsightType.RECOMMENDATIONS)
        insights_md = generator.generate_insights(
            fig=fig,
            insight_types=insight_types,
            business_context=payload.context,
            tone="professional",
        )
        return ChartInsightsResponse(insights_md=insights_md)
    except Exception:
        pass

    def _coerce_num(arr):
        try:
            s = pd.Series(arr)
            # Handle numeric-like strings such as "1,234" or "10%"
            s = pd.to_numeric(s.astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")
            return s
        except Exception:
            return pd.Series([], dtype=float)

    def _top_n_pairs(x, y, n=5):
        s = pd.Series(y, index=pd.Index(x, name="label"))
        s = pd.to_numeric(s, errors="coerce").fillna(0)
        top = s.sort_values(ascending=False).head(n)
        return list(top.items())

    def _safe_get(tr: dict, key: str, alt_key: str | None = None):
        v = tr.get(key)
        if v is None and alt_key is not None:
            v = tr.get(alt_key)
        return v if v is not None else []

    def _get_bar_numeric_and_labels(tr):
        orientation = (tr.get("orientation") or "v").lower()
        x = _safe_get(tr, "x")
        y = _safe_get(tr, "y")
        if orientation == "h":
            nums = _coerce_num(x)
            labels = y
        else:
            nums = _coerce_num(y)
            labels = x
        # Fallbacks if nums are all NaN
        if nums.dropna().empty:
            nums = _coerce_num(_safe_get(tr, "text"))
        if nums.dropna().empty:
            nums = _coerce_num(_safe_get(tr, "values"))
        cd = tr.get("customdata")
        if nums.dropna().empty and isinstance(cd, (list, tuple, np.ndarray)):
            try:
                # Try first column of customdata if it's 2D
                cd_list = cd.tolist() if isinstance(cd, np.ndarray) else cd
                if cd_list and isinstance(cd_list[0], (list, tuple)):
                    nums = _coerce_num([row[0] for row in cd_list])
                else:
                    nums = _coerce_num(cd_list)
            except Exception:
                pass
        return nums, labels

    # Heuristic extraction across traces
    data = fig.get("data", []) or []
    findings: list[str] = []
    recs: list[str] = []

    if not data:
        insights_md = f"## {title}\n\n- **Summary**: No data provided. Please render a chart first."
        return ChartInsightsResponse(insights_md=insights_md)

    # Aggregate stats across numeric series
    series_stats = []
    all_trace_names: list[str] = []
    for tr in data:
        ttype = (tr.get("type") or tr.get("_type") or "").lower()
        name = tr.get("name") or ttype or "series"
        x = _safe_get(tr, "x")
        y = _safe_get(tr, "y")
        all_trace_names.append(name)
        if ttype in ("bar", "funnel"):
            nums, labels = _get_bar_numeric_and_labels(tr)
            if not nums.dropna().empty:
                series_stats.append({
                    "name": name,
                    "count": int(nums.count()),
                    "sum": float(nums.sum()),
                    "mean": float(nums.mean()),
                    "min": float(nums.min()),
                    "max": float(nums.max()),
                })
                if labels and len(labels) == len(nums):
                    top = _top_n_pairs(labels, list(nums.fillna(0).values), n=3)
                    if top:
                        findings.append(
                            f"Top contributors in {name}: " + ", ".join([f"{lbl} ({val:.0f})" for lbl, val in top])
                        )
        elif ttype in ("scatter", "line", "scattergl"):
            ys = _coerce_num(y)
            if ys.dropna().empty and x:
                # Some lines may be horizontal with numeric x
                ys = _coerce_num(x)
            if not ys.dropna().empty:
                series_stats.append({
                    "name": name,
                    "count": int(ys.count()),
                    "sum": float(ys.sum()),
                    "mean": float(ys.mean()),
                    "min": float(ys.min()),
                    "max": float(ys.max()),
                })
        elif ttype == "histogram":
            xs = _coerce_num(x)
            if not xs.dropna().empty:
                series_stats.append({
                    "name": name,
                    "count": int(xs.count()),
                    "mean": float(xs.mean()),
                    "min": float(xs.min()),
                    "max": float(xs.max()),
                    "sum": float(xs.sum()),
                })
        elif ttype in ("box", "violin"):
            ys = _coerce_num(y)
            if not ys.dropna().empty:
                series_stats.append({
                    "name": name,
                    "count": int(ys.count()),
                    "mean": float(ys.mean()),
                    "min": float(ys.min()),
                    "max": float(ys.max()),
                })
        elif ttype == "heatmap":
            z = _safe_get(tr, "z")
            try:
                zarr = np.array(z, dtype=float)
                if np.isfinite(zarr).any():
                    total = float(np.nansum(zarr))
                    mx = float(np.nanmax(zarr)) if np.isfinite(zarr).any() else 0.0
                    series_stats.append({
                        "name": name,
                        "sum": total,
                        "max": mx,
                    })
                    # Hotspot labels if x/y provided
                    xi = _safe_get(tr, "x")
                    yi = _safe_get(tr, "y")
                    if isinstance(zarr, np.ndarray) and zarr.ndim == 2 and xi and yi:
                        # Find top 3 cells
                        idx = np.dstack(np.unravel_index(np.argsort(-zarr, axis=None)[:3], zarr.shape))[0]
                        labels = []
                        for r, c in idx:
                            try:
                                labels.append(f"{yi[r]} / {xi[c]} ({zarr[r, c]:.0f})")
                            except Exception:
                                pass
                        if labels:
                            findings.append("Heatmap hotspots: " + ", ".join(labels))
            except Exception:
                pass
        elif ttype in ("scatterpolar", "barpolar"):
            # Polar/radar charts: values in r, labels in theta
            r_vals = _safe_get(tr, "r")
            theta_vals = _safe_get(tr, "theta", alt_key="labels")
            rs = _coerce_num(r_vals)
            if not rs.dropna().empty:
                series_stats.append({
                    "name": name,
                    "count": int(rs.count()),
                    "sum": float(rs.sum()),
                    "mean": float(rs.mean()),
                    "min": float(rs.min()),
                    "max": float(rs.max()),
                })
                if theta_vals and len(theta_vals) == len(rs):
                    top = _top_n_pairs(theta_vals, list(rs.fillna(0).values), n=3)
                    if top:
                        findings.append(
                            f"Top categories in {name}: " + ", ".join([f"{lbl} ({val:.0f})" for lbl, val in top])
                        )
        elif ttype == "pie":
            labels = _safe_get(tr, "labels")
            values = _safe_get(tr, "values")
            if labels and values and len(labels) == len(values):
                top = _top_n_pairs(labels, values, n=3)
                total = float(pd.to_numeric(pd.Series(values), errors="coerce").fillna(0).sum())
                share = ", ".join([f"{lbl} ({(val/total*100 if total>0 else 0):.1f}%)" for lbl, val in top])
                findings.append(f"Largest slices: {share}")
        elif ttype == "indicator":
            val = tr.get("value")
            try:
                v = float(val)
                findings.append(f"Current value: {v:,.0f}")
            except Exception:
                pass

    # Trend detection for lines/scatters (first numeric series)
    for tr in data:
        ttype = (tr.get("type") or "").lower()
        if ttype in ("scatter", "line", "scattergl"):
            y = tr.get("y") or []
            ys = _coerce_num(y)
            if ys.dropna().empty or len(ys) < 2:
                continue
            slope = ys.diff().mean()
            if pd.notna(slope):
                if slope > 0:
                    findings.append("Upward trend observed over time.")
                elif slope < 0:
                    findings.append("Downward trend observed over time.")
            break

    # If nothing numeric was found, still return a helpful summary
    if not series_stats:
        parts = [f"## {title}"]
        parts.append(f"- **Traces detected**: {len(data)} — " + ", ".join([str(n) for n in all_trace_names[:10]]))
        parts.append("- **Summary**: The chart data does not contain numeric values I can analyze reliably (y/x/text/values/customdata are non-numeric or empty).")
        parts.append("\n### Recommendations")
        parts.append("- **Action**: Ensure numeric fields are provided for metrics like Count, Severity (as scores/buckets mapped to scores), Risk, Cost, or Manhours.")
        parts.append("- **Action**: If values are strings (e.g., '10'), keep them numeric or pass as numbers in Plotly traces.")
        parts.append("- **Action**: For stacked bars, include numeric arrays in `y` (vertical) or `x` (horizontal). Optionally set `orientation` to clarify.")
        base_md = "\n".join(parts)

    # Optional LLM refinement to produce layman-friendly prose
    try:
        context_chunks = [
            f"Title: {title}",
            f"User context: {(payload.context or '').strip() or 'N/A'}",
            "Heuristic summary:\n" + base_md,
        ]
        llm_md = ask_openai(
            "Rewrite the heuristic chart summary into a clear, layman-friendly report. Use Markdown with sections: Summary, Key Insights (bullets), Recommendations (bullets). Keep it concise and avoid jargon.",
            context="\n\n".join(context_chunks),
            model="gpt-4o",
            code_mode=False,
            multi_df=False,
        )
        if llm_md and not llm_md.lower().startswith("openai") and "not installed" not in llm_md.lower():
            return ChartInsightsResponse(insights_md=llm_md)
    except Exception:
        pass

    return ChartInsightsResponse(insights_md=base_md)


# ---------- Chart-specific AI insights (GET) ----------

def _build_chart_figure(chart: str, dataset: str = "incident", event_type: str = "Incidents"):
    chart_l = (chart or "").strip().lower()
    ds_l = (dataset or "incident").strip().lower()
    # Load common dataframes
    inc = get_incident_df()
    haz = get_hazard_df()
    aud = get_audit_df()
    ins = get_inspection_df()

    # Map chart name to figure
    if chart_l in ("hse-scorecard", "scorecard"):
        fig = plot_service.create_unified_hse_scorecard(inc, haz, aud, ins)
        title = "HSE Scorecard"
        return fig, title
    if chart_l in ("hse-performance-index", "performance-index"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_hse_performance_index(df)
        title = "HSE Performance Index"
        return fig, title
    if chart_l in ("psm-breakdown", "psm"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_psm_breakdown(df)
        title = "PSM Breakdown"
        return fig, title
    if chart_l in ("data-quality-metrics", "data-quality"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_data_quality_metrics(df)
        title = "Data Quality Metrics"
        return fig, title
    if chart_l in ("audit-inspection-tracker", "audit-tracker"):
        fig = plot_service.create_audit_inspection_tracker(aud, ins)
        title = "Audit & Inspection Tracker"
        return fig, title
    if chart_l in ("location-risk-treemap", "location-treemap"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_location_risk_treemap(df)
        title = "Location Risk Treemap"
        return fig, title
    if chart_l in ("violation-analysis", "violation"):
        # default hazard
        df = haz if ds_l == "hazard" else inc
        fig = plot_service.create_violation_analysis(df)
        title = "Violation Analysis"
        return fig, title
    if chart_l in ("cost-prediction-analysis", "cost-prediction"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_cost_prediction_analysis(df)
        title = "Cost Prediction Analysis"
        return fig, title
    if chart_l in ("facility-layout-heatmap", "layout-heatmap"):
        fig = plot_service.create_facility_layout_heatmap(inc, haz)
        title = "Facility Layout Heatmap"
        return fig, title
    if chart_l in ("facility-3d-heatmap", "3d-heatmap"):
        df = inc if ds_l == "incident" else haz
        fig = plot_service.create_3d_facility_heatmap(df, event_type=event_type or ("Incidents" if ds_l == "incident" else "Hazards"))
        title = "Facility 3D Heatmap"
        return fig, title
    raise ValueError(f"Unknown chart: {chart}")


@router.get("/insights/{chart}", response_model=ChartInsightsResponse)
async def insights_for_chart(chart: str, dataset: str = Query("incident"), event_type: str = Query("Incidents")) -> ChartInsightsResponse:
    """Build the specified chart using current data, then generate AI insights for it.
    Returns only the AI-generated insights (Markdown) to the client.
    """
    try:
        fig, title = _build_chart_figure(chart, dataset=dataset, event_type=event_type)
    except Exception as e:
        return ChartInsightsResponse(insights_md=f"## {chart}\n\n- **Error**: {e}")

    # Reuse the chart-based insights generator
    payload = ChartInsightsRequest(figure=fig.to_plotly_json(), title=title)
    resp = await generate_chart_insights(payload)  # type: ignore[arg-type]
    return resp


@router.post("/insights/from-data", response_model=ChartInsightsResponse)
async def generate_data_insights(payload: DataInsightsRequest) -> ChartInsightsResponse:
    """Data-driven insights that do not rely on chart structure. Deterministic and robust.
    Accepts records plus optional column mappings.
    """
    title = payload.title or "Insights"
    df = payload_to_df(payload.data.records) if payload and payload.data else pd.DataFrame()
    if df is None or df.empty:
        return ChartInsightsResponse(insights_md=f"## {title}\n\n- **Summary**: No data provided.")

    def _pick(colnames: list[str]) -> str | None:
        for c in colnames:
            if c in df.columns:
                return c
        return None

    # Infer columns if not provided
    time_col = payload.time_col or _pick([
        "date", "occurrence_date", "entered_date", "reported_date", "created_date", "start_date", "scheduled_date",
    ])
    cat_col = payload.category_col or _pick([
        "department", "dept", "category", "location", "site", "area",
    ])

    metrics = [m.lower() for m in (payload.metrics or ["count", "severity", "risk", "cost", "manhours"])]
    value_cols = payload.value_cols or {}
    sev_col = value_cols.get("severity") or _pick(["severity_score", "severity", "severity_level"])  # numeric preferred
    risk_col = value_cols.get("risk") or _pick(["risk_score", "risk", "risk_level"])  # numeric preferred
    cost_col = value_cols.get("cost") or _pick(["cost", "estimated_cost", "cost_usd", "cost_inr"])  # numeric
    mh_col = value_cols.get("manhours") or _pick(["manhours", "man_hours", "man_hrs", "hours"])  # numeric

    # Coerce numeric columns safely
    for c in [sev_col, risk_col, cost_col, mh_col]:
        if c and c in df.columns:
            try:
                df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", "").str.replace("%", ""), errors="coerce")
            except Exception:
                df[c] = pd.to_numeric(df[c], errors="coerce")

    # Coerce time column
    if time_col and time_col in df.columns:
        try:
            df["__dt"] = pd.to_datetime(df[time_col], errors="coerce")
        except Exception:
            df["__dt"] = pd.NaT
    else:
        df["__dt"] = pd.NaT

    parts: list[str] = [f"## {title}"]

    # Summary block
    parts.append(f"- **Rows**: {len(df):,}")
    if df["__dt"].notna().any():
        dmin = df["__dt"].min()
        dmax = df["__dt"].max()
        try:
            parts.append(f"- **Date range**: {dmin.date().isoformat()} to {dmax.date().isoformat()}")
        except Exception:
            parts.append("- **Date range**: available")

    # Top contributors by category
    if cat_col and cat_col in df.columns:
        vc = (
            df[cat_col].astype(str).str.strip().replace({"": "Unknown"}).value_counts().head(payload.top_n)
        )
        if not vc.empty:
            parts.append("\n### Top contributors")
            for idx, val in vc.items():
                parts.append(f"- **{idx}**: {int(val):,}")

    # Metric stats
    def _metric_block(name: str, col: str | None):
        if not col or col not in df.columns:
            return
        s = pd.to_numeric(df[col], errors="coerce")
        if s.notna().sum() == 0:
            return
        parts.append(f"\n### {name.title()} statistics")
        parts.append(f"- **Mean**: {float(s.mean()):,.2f}")
        parts.append(f"- **Min/Max**: {float(s.min()):,.2f} / {float(s.max()):,.2f}")
        if cat_col and cat_col in df.columns:
            grp = s.groupby(df[cat_col].astype(str).str.strip().replace({"": "Unknown"})).mean().sort_values(ascending=False).head(3)
            if not grp.empty:
                tops = ", ".join([f"{k} ({v:,.2f})" for k, v in grp.items()])
                parts.append(f"- **Top by {name} (avg)**: {tops}")

    if "severity" in metrics:
        _metric_block("severity", sev_col)
    if "risk" in metrics:
        _metric_block("risk", risk_col)
    if "cost" in metrics:
        _metric_block("cost", cost_col)
    if "manhours" in metrics:
        _metric_block("manhours", mh_col)

    # Trend analysis (monthly counts)
    if df["__dt"].notna().any():
        monthly = df.dropna(subset=["__dt"]).copy()
        monthly["__ym"] = monthly["__dt"].dt.to_period("M").dt.to_timestamp()
        cnt = monthly.groupby("__ym").size().sort_index()
        if len(cnt) >= 3:
            last3 = cnt.tail(3).values
            if len(set(last3)) > 1:
                pct = (last3[-1] - last3[0]) / max(1, last3[0]) * 100.0
                direction = "up" if pct > 0 else "down"
                parts.append(f"\n### Trend")
                parts.append(f"- **Monthly count trend**: {direction} {abs(pct):.1f}% over last 3 months")

    # Data quality
    dq_notes: list[str] = []
    for name, col in [("severity", sev_col), ("risk", risk_col), ("cost", cost_col), ("manhours", mh_col)]:
        if col and col in df.columns:
            miss = df[col].isna().sum()
            rate = miss / len(df) * 100.0 if len(df) else 0.0
            if rate >= 30.0:
                dq_notes.append(f"- **{name}** missing {rate:.0f}% — improve capture to strengthen insights.")
    if dq_notes:
        parts.append("\n### Data quality")
        parts.extend(dq_notes)

    return ChartInsightsResponse(insights_md="\n".join(parts))
