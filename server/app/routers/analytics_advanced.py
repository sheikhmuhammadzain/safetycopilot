"""
Advanced Analytics Router
Implements critical HSE analytics including Heinrich's Pyramid, KPIs, and predictive analytics.
Built with professional data science practices and best engineering standards.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import re
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import JSONResponse

from ..services.excel import get_incident_df, get_hazard_df, get_audit_df, get_inspection_df, load_default_sheets
from ..services.json_utils import to_native_json


router = APIRouter(prefix="/analytics/advanced", tags=["advanced-analytics"])


# ======================= HELPER FUNCTIONS =======================

def _resolve_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """Resolve column name from list of candidates (case-insensitive, flexible matching)."""
    if df is None or df.empty:
        return None
    col_map = {str(c).strip().lower(): c for c in df.columns}
    for candidate in candidates:
        key = str(candidate).strip().lower()
        if key in col_map:
            return col_map[key]
    # Relaxed contains match
    for candidate in candidates:
        key = str(candidate).strip().lower()
        for lk, orig in col_map.items():
            if key in lk:
                return orig
    return None


def _apply_filters(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    location: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
) -> pd.DataFrame:
    """Apply common filters to dataframe."""
    if df is None or df.empty:
        return df
    
    filtered = df.copy()
    
    # Date range filter
    if start_date or end_date:
        date_col = _resolve_column(filtered, ["occurrence_date", "date", "start_date", "reported_date"])
        if date_col:
            dates = pd.to_datetime(filtered[date_col], errors="coerce")
            if start_date:
                mask = dates >= pd.to_datetime(start_date)
                filtered = filtered.loc[mask]
            if end_date:
                mask = dates <= pd.to_datetime(end_date)
                filtered = filtered.loc[mask]
    
    # Location filter
    if location is not None and location != "":
        loc_col = _resolve_column(filtered, ["location", "audit_location", "finding_location"])
        if loc_col:
            filtered = filtered[
                filtered[loc_col].astype(str).str.contains(str(location), case=False, na=False)
            ]
    
    # Department filter
    if department is not None and department != "":
        dept_col = _resolve_column(filtered, ["department", "section", "sub_department"])
        if dept_col:
            filtered = filtered[
                filtered[dept_col].astype(str).str.contains(str(department), case=False, na=False)
            ]
    
    # Status filter
    if status is not None and status != "":
        status_col = _resolve_column(filtered, ["status", "incident_status", "audit_status", "hazard_status"])
        if status_col:
            filtered = filtered[
                filtered[status_col].astype(str).str.contains(str(status), case=False, na=False)
            ]
    
    return filtered


def _classify_severity_level(severity_score: Any, severity_text: Any = None) -> str:
    """
    Classify severity into Heinrich Pyramid layers:
    - Layer 1: Fatality/Serious Injury (severity >= 4 or 'Critical'/'Severe')
    - Layer 2: Minor Injury (severity 2-3 or 'Serious'/'High')
    - Layer 3: First Aid/Near Miss (severity 1 or 'Minor'/'Low')
    - Layer 4: Unsafe Condition (from hazards)
    - Layer 5: At-Risk Behavior (from observations/audits)
    """
    # Try text-based classification first
    if severity_text and pd.notna(severity_text):
        text = str(severity_text).lower().strip()
        if any(k in text for k in ["critical", "fatal", "severe", "c4", "c3"]):
            return "Serious Injury/Fatality"
        if any(k in text for k in ["serious", "high", "c2", "moderate"]):
            return "Minor Injury"
        if any(k in text for k in ["minor", "low", "c1", "first aid", "near miss"]):
            return "First Aid/Near Miss"
    
    # Numeric classification
    try:
        score = float(severity_score)
        if score >= 3:
            return "Serious Injury/Fatality"
        elif score >= 2:
            return "Minor Injury"
        else:
            return "First Aid/Near Miss"
    except (ValueError, TypeError):
        pass
    
    return "First Aid/Near Miss"  # Default to least severe


def _calculate_near_miss_ratio(incidents_df: pd.DataFrame, hazards_df: pd.DataFrame) -> float:
    """Calculate near-miss to incident ratio (industry standard: 1 incident : 10 near-misses)."""
    if incidents_df is None or incidents_df.empty:
        return 0.0
    
    incident_count = len(incidents_df)
    near_miss_count = 0
    
    # Count near-misses from incidents
    if "incident_type" in incidents_df.columns:
        near_miss_count += incidents_df["incident_type"].astype(str).str.contains(
            "near miss|near-miss|nearmiss", case=False, na=False
        ).sum()
    
    # Count hazards as potential near-misses
    if hazards_df is not None and not hazards_df.empty:
        near_miss_count += len(hazards_df)
    
    if incident_count == 0:
        return 0.0
    
    return round(near_miss_count / incident_count, 2)


# ======================= HEINRICH'S SAFETY PYRAMID =======================

def _classify_heinrich_level(row: pd.Series) -> tuple:
    """
    Classify incident into Heinrich pyramid level based on consequence severity.
    
    Returns:
        tuple: (level, description)
        - Level 1: Fatalities (C4-C5 Injuries)
        - Level 2: Serious Injuries (C3)
        - Level 3: Minor Injuries (C1-C2)
        - Level 4: Near Misses (C0 actual with C3-C5 worst)
        - Level 5: Unsafe Conditions (from hazards/audits)
    """
    actual = str(row.get('actual_consequence_incident', '')).strip()
    worst = str(row.get('worst_case_consequence_incident', '')).strip()
    inc_type = str(row.get('incident_type', '')).lower().strip()
    
    # Level 1: Fatalities (C4-C5 Injuries)
    if 'injury' in inc_type and any(x in actual for x in ['C4', 'C5', 'c4', 'c5', 'Major', 'Catastrophic']):
        return (1, 'Fatalities (C4 and C5 Injuries)')
    
    # Level 2: Serious Injuries (C3)
    if 'injury' in inc_type and any(x in actual for x in ['C3', 'c3', 'Severe']):
        return (2, 'Serious Injuries (C3)')
    
    # Level 3: Minor Injuries (C1-C2)
    if 'injury' in inc_type and any(x in actual for x in ['C1', 'C2', 'c1', 'c2', 'Minor', 'Serious']):
        return (3, 'Minor Injuries (C1 and C2)')
    
    # Level 4: Near Misses (C0 actual with C3-C5 worst)
    if any(x in actual for x in ['C0', 'c0']) and any(x in worst for x in ['C3', 'C4', 'C5', 'c3', 'c4', 'c5']):
        return (4, 'Near Misses (C0 actual, C3 to C5 worst)')
    
    return (None, None)


@router.get("/heinrich-pyramid")
async def heinrich_safety_pyramid():
    """
    Heinrich's Safety Pyramid - exact implementation matching reference logic.
    """
    # Load sheets directly by name (matching test script)
    sheets = load_default_sheets()
    incident_df = sheets.get('Incident')
    hazard_df = sheets.get('Hazard ID')
    audit_df = sheets.get('Audit Findings')
    
    # Clean column names (strip only)
    for df in [incident_df, hazard_df, audit_df]:
        if df is not None and not df.empty:
            df.columns = df.columns.str.strip()
    
    # Classification function for incidents (exact match to reference)
    def classify_heinrich_level(row):
        actual = str(row.get('Actual Consequence (Incident)', '')).strip()
        worst = str(row.get('Worst Case Consequence (Incident)', '')).strip()
        inc_type = str(row.get('Incident Type(s)', '')).lower().strip()

        if inc_type == 'injury' and actual in ['C4 - Major', 'C5 - Catastrophic']:
            return 1, 'Fatality (C4–C5 Injury)'
        elif inc_type == 'injury' and actual == 'C3 - Severe':
            return 2, 'Serious Injury (C3)'
        elif inc_type == 'injury' and actual in ['C1 - Minor', 'C2 - Serious']:
            return 3, 'Minor Injury (C1–C2)'
        elif actual.startswith('C0') and any(x in worst for x in ['C3', 'C4', 'C5']):
            return 4, 'Near Miss (C0 actual, C3–C5 worst)'
        return None, None
    
    # Apply classification to incidents
    if incident_df is not None and not incident_df.empty:
        incident_df[['Heinrich_Level', 'Heinrich_Desc']] = incident_df.apply(
            classify_heinrich_level, axis=1, result_type='expand'
        )
    
    # Hazards as Unsafe Conditions
    if hazard_df is not None and not hazard_df.empty:
        def _is_hazard_level5(x):
            val = str(x).strip()
            # Exact match including case variations
            return val in ['C1 - Minor', 'C2 - Serious']
        
        hazard_df['Heinrich_Level'] = hazard_df['Worst Case Consequence Potential (Hazard ID)'].apply(
            lambda x: 5 if _is_hazard_level5(x) else None
        )
        hazard_df['Heinrich_Desc'] = hazard_df['Heinrich_Level'].apply(
            lambda x: 'Unsafe Condition (Hazard)' if x == 5 else None
        )
    
    # Audits as Unsafe Conditions (Level 5)
    if audit_df is not None and not audit_df.empty:
        def _is_audit_level5(x):
            val = str(x).strip()
            # Check if string contains C1 - Minor or C2 - Serious (handles semicolon-separated values)
            return 'C1 - Minor' in val or 'C2 - Serious' in val
        
        audit_df['Heinrich_Level'] = audit_df['Worst Case Consequence'].apply(
            lambda x: 5 if _is_audit_level5(x) else None
        )
        audit_df['Heinrich_Desc'] = audit_df['Heinrich_Level'].apply(
            lambda x: 'Unsafe Condition (Audit)' if x == 5 else None
        )
    
    # Combine all data (exact approach from reference)
    combined = pd.concat([
        incident_df.dropna(subset=['Heinrich_Level'])[['Heinrich_Level', 'Heinrich_Desc']] if incident_df is not None else pd.DataFrame(),
        hazard_df.dropna(subset=['Heinrich_Level'])[['Heinrich_Level', 'Heinrich_Desc']] if hazard_df is not None else pd.DataFrame(),
        audit_df.dropna(subset=['Heinrich_Level'])[['Heinrich_Level', 'Heinrich_Desc']] if audit_df is not None else pd.DataFrame()
    ], ignore_index=True)
    
    # Predefine all levels with zero counts (red to green safety gradient)
    all_levels = pd.DataFrame({
        'Heinrich_Level': [1, 2, 3, 4, 5],
        'Description': [
            'Fatalities (C4 and C5 Injuries)',
            'Serious Injuries (C3)',
            'Minor Injuries (C1 and C2)',
            'Near Misses (C0 actual, C3 to C5 worst)',
            'Unsafe Conditions (Hazards + Audit Findings)'
        ],
        'Color_Code': ['#DC3545', '#FD7E14', '#FFC107', '#28A745', '#20C997']
    })
    
    # Summarize actual counts
    if not combined.empty:
        heinrich_summary = (
            combined.groupby('Heinrich_Level')
            .size()
            .reset_index(name='Count')
            .sort_values('Heinrich_Level')
        )
    else:
        heinrich_summary = pd.DataFrame(columns=['Heinrich_Level', 'Count'])
    
    # Merge with all levels, filling missing counts with 0
    heinrich_summary = all_levels.merge(heinrich_summary, on='Heinrich_Level', how='left').fillna({'Count': 0})
    
    # Calculate percentages
    total = heinrich_summary['Count'].sum()
    if total > 0:
        heinrich_summary['Percent'] = (heinrich_summary['Count'] / total * 100).round(1)
    else:
        heinrich_summary['Percent'] = 0.0
    
    # Convert to JSON-style list (exact output format)
    result = heinrich_summary.to_dict(orient='records')
    
    return JSONResponse(content=to_native_json(result))


@router.get("/hse-metrics")
async def hse_metrics():
    """
    Calculate HSE metrics including incidents, near-miss ratio, and injury statistics.
    """
    # Load sheets directly by name
    sheets = load_default_sheets()
    incident_df = sheets.get('Incident')
    hazard_df = sheets.get('Hazard ID')
    audit_df = sheets.get('Audit Findings')
    
    # Clean column names
    for df in [incident_df, hazard_df, audit_df]:
        if df is not None and not df.empty:
            df.columns = df.columns.str.strip()
    
    # Initialize metrics
    fatalities = 0
    serious_injuries = 0
    recordable_injuries = 0
    near_misses = 0
    at_risk_behaviors = 0
    total_incidents = 0
    injuries_total = 0
    
    # Calculate from incidents
    if incident_df is not None and not incident_df.empty:
        total_incidents = len(incident_df)
        
        # Filter injuries
        injuries = incident_df[
            incident_df['Incident Type(s)'].str.lower().str.strip() == 'injury'
        ]
        injuries_total = len(injuries)
        
        # Fatalities (C4-C5)
        fatalities = len(injuries[
            injuries['Actual Consequence (Incident)'].isin(['C4 - Major', 'C5 - Catastrophic'])
        ])
        
        # Serious Injuries (C3)
        serious_injuries = len(injuries[
            injuries['Actual Consequence (Incident)'] == 'C3 - Severe'
        ])
        
        # Recordable Injuries (C2-C5)
        recordable_injuries = len(injuries[
            injuries['Actual Consequence (Incident)'].isin(['C2 - Serious', 'C3 - Severe', 'C4 - Major', 'C5 - Catastrophic'])
        ])
        
        # Near Misses (C0 actual with C3-C5 worst)
        near_misses = len(incident_df[
            (incident_df['Actual Consequence (Incident)'].astype(str).str.startswith('C0', na=False)) &
            (incident_df['Worst Case Consequence (Incident)'].astype(str).str.contains('C3|C4|C5', na=False))
        ])
    
    # Calculate at-risk behaviors (Unsafe Conditions)
    if hazard_df is not None and not hazard_df.empty:
        at_risk_behaviors += len(hazard_df[
            hazard_df['Worst Case Consequence Potential (Hazard ID)'].astype(str).str.strip().isin(['C1 - Minor', 'C2 - Serious'])
        ])
    
    if audit_df is not None and not audit_df.empty:
        at_risk_behaviors += len(audit_df[
            audit_df['Worst Case Consequence'].astype(str).str.strip().isin(['C1 - Minor', 'C2 - Serious'])
        ])
    
    # Calculate near-miss ratio
    near_miss_ratio = f"{near_misses / injuries_total:.2f}:1" if injuries_total > 0 else "N/A"
    
    result = {
        "total_incidents": total_incidents,
        "near_miss_ratio": near_miss_ratio,
        "fatality_actual": fatalities,
        "lost_workday_cases_actual": serious_injuries,
        "recordable_injuries_actual": recordable_injuries,
        "near_misses_actual": near_misses,
        "unsafe_condition": at_risk_behaviors,
    }
    
    return JSONResponse(content=to_native_json(result))


@router.get("/injury-risk-by-department")
async def injury_risk_by_department():
    """
    Compute ISO 45001-style injury risk per Department using exact column names:
    - Filter Incidents where 'Incident Type(s)' == 'injury'
    - Severity mapping to scores (C0..C5)
    - Likelihood from department injury count quintiles (1..5)
    - Risk_Score = (0.8 * Sum_Actual_Severity + 0.2 * Sum_Worst_Severity) * Likelihood
    - Normalized_Score = min-max normalization of Risk_Score

    Returns shape compatible with ShadcnBarCard:
    { labels: string[], series: [{name, data}...], table: [...], meta: {...} }
    """
    sheets = load_default_sheets()
    inc = sheets.get('Incident')
    if inc is None or inc.empty:
        return JSONResponse(content=to_native_json({
            "labels": [],
            "series": [],
            "table": [],
            "meta": {"records_used": 0, "sheet": 'Incident'}
        }))

    # Strip column names and values
    inc = inc.copy()
    inc.columns = inc.columns.str.strip()

    # Ensure required columns exist
    required_cols = [
        'Incident Number',
        'Incident Type(s)',
        'Actual Consequence (Incident)',
        'Worst Case Consequence (Incident)',
        'Department',
    ]
    for c in required_cols:
        if c not in inc.columns:
            # Try to resolve by case-insensitive match
            matches = [col for col in inc.columns if str(col).strip().lower() == c.lower()]
            if matches:
                inc.rename(columns={matches[0]: c}, inplace=True)

    # Filter injuries
    injuries_df = inc[
        inc['Incident Number'].notna()
        & inc['Incident Type(s)'].notna()
        & (inc['Incident Type(s)'].astype(str).str.strip().str.lower() == 'injury')
    ].copy()

    if injuries_df.empty:
        return JSONResponse(content=to_native_json({
            "labels": [],
            "series": [],
            "table": [],
            "meta": {"records_used": 0, "sheet": 'Incident'}
        }))

    # ISO 45001-based severity scores
    severity_scores = {
        'C0 - No Ill Effect': 1,
        'C1 - Minor': 2,
        'C2 - Serious': 3,
        'C3 - Severe': 4,
        'C4 - Major': 5,
        'C5 - Catastrophic': 5,
    }

    injuries_df['Department'] = injuries_df['Department'].astype(str).replace({'': 'Unknown', 'nan': 'Unknown'})

    injuries_df['Actual_Severity'] = injuries_df['Actual Consequence (Incident)'].map(severity_scores).fillna(0)
    injuries_df['Worst_Severity'] = injuries_df['Worst Case Consequence (Incident)'].map(severity_scores).fillna(0)

    # Injury counts per department -> Likelihood quintiles
    injury_counts = injuries_df.groupby('Department').size().reset_index(name='Injury_Count')
    if len(injury_counts) > 1:
        qs = injury_counts['Injury_Count'].quantile([0.2, 0.4, 0.6, 0.8]).values
    else:
        qs = [1, 1, 1, 1]

    def assign_likelihood(count: float) -> int:
        if count <= qs[0]:
            return 1
        elif count <= qs[1]:
            return 2
        elif count <= qs[2]:
            return 3
        elif count <= qs[3]:
            return 4
        else:
            return 5

    injury_counts['Likelihood'] = injury_counts['Injury_Count'].apply(assign_likelihood)

    # Aggregate by department
    dept_summary = injuries_df.groupby('Department').agg(
        Injury_Count=('Incident Number', 'count'),
        Sum_Actual_Severity=('Actual_Severity', 'sum'),
        Sum_Worst_Severity=('Worst_Severity', 'sum'),
    ).reset_index()

    dept_summary = dept_summary.merge(injury_counts[['Department', 'Likelihood']], on='Department', how='left')

    dept_summary['Risk_Score'] = (
        0.8 * dept_summary['Sum_Actual_Severity'] + 0.2 * dept_summary['Sum_Worst_Severity']
    ) * dept_summary['Likelihood']

    # Normalization
    min_score = float(dept_summary['Risk_Score'].min()) if len(dept_summary) else 0.0
    max_score = float(dept_summary['Risk_Score'].max()) if len(dept_summary) else 0.0
    if max_score != min_score:
        dept_summary['Normalized_Score'] = (dept_summary['Risk_Score'] - min_score) / (max_score - min_score)
    else:
        dept_summary['Normalized_Score'] = 0.0

    # Sort by normalized desc
    dept_summary = dept_summary.sort_values(by='Normalized_Score', ascending=False)

    labels = dept_summary['Department'].astype(str).tolist()
    series = [
        {"name": "Normalized Injury Risk Score", "data": dept_summary['Normalized_Score'].round(3).tolist()},
        {"name": "Injury Risk Score", "data": dept_summary['Risk_Score'].round(3).tolist()},
    ]

    table = dept_summary[[
        'Department', 'Injury_Count', 'Sum_Actual_Severity', 'Sum_Worst_Severity', 'Likelihood', 'Risk_Score', 'Normalized_Score'
    ]].round(3).to_dict(orient='records')

    payload = {
        "labels": labels,
        "x": labels,  # compat with other clients
        "series": series,
        "table": table,
        "meta": {"records_used": int(len(injuries_df)), "sheet": 'Incident'},
    }

    return JSONResponse(content=to_native_json(payload))


@router.get("/heinrich-pyramid-breakdown")
async def heinrich_pyramid_breakdown(
    start_date: Optional[str] = Query(None, description="Filter start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Filter end date (YYYY-MM-DD)"),
):
    """
    Detailed breakdown of Heinrich's Pyramid by Department and Location.
    
    Shows contribution of each department and location to pyramid layers:
    - Fatality (Incident sheet: severity_score >= 4-5 OR consequence contains 'fatal')
    - Lost Workday Cases (Incident sheet: severity_score >= 3)
    - Recordable Injuries (Incident sheet: severity_score >= 2)
    - Near Misses (Hazard ID sheet + Incident sheet with 'near miss' type)
    - At-Risk Behaviors (Audit + Inspection sheets with findings)
    
    Data Sources:
    - Incidents: Incident sheet
    - Hazards: Hazard ID sheet
    - Audits: Audit Findings sheet
    - Inspections: Inspection Findings sheet
    """
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    aud_df = get_audit_df()
    insp_df = get_inspection_df()
    
    # Apply date filters
    inc_df = _apply_filters(inc_df, start_date, end_date, None, None)
    haz_df = _apply_filters(haz_df, start_date, end_date, None, None)
    
    breakdown = {
        "by_department": [],
        "by_location": [],
        "data_sources": {
            "fatalities": "Incident sheet (severity_score >= 4-5 OR actual/worst_consequence contains 'fatal')",
            "lost_workday_cases": "Incident sheet (severity_score >= 3, excluding fatalities)",
            "recordable_injuries": "Incident sheet (severity_score >= 2, excluding LTI and fatalities)",
            "near_misses": "Hazard ID sheet + Incident sheet (incident_type contains 'near miss')",
            "at_risk_behaviors": "Audit Findings sheet + Inspection Findings sheet (non-null findings)"
        }
    }
    
    # Department breakdown
    if inc_df is not None and not inc_df.empty:
        dept_col = _resolve_column(inc_df, ["department", "sub_department"])
        sev_col = _resolve_column(inc_df, ["severity_score", "severity"])
        act_cons = _resolve_column(inc_df, ["actual_consequence_incident"])
        worst_cons = _resolve_column(inc_df, ["worst_case_consequence_incident"])
        type_col = _resolve_column(inc_df, ["incident_type", "category"])
        
        if dept_col and dept_col in inc_df.columns:
            for dept in inc_df[dept_col].dropna().unique():
                dept_inc = inc_df[inc_df[dept_col] == dept]
                
                # Calculate layers for this department
                fatalities = 0
                lost_workday = 0
                recordable = 0
                
                if sev_col and sev_col in dept_inc.columns:
                    sev_vals = pd.to_numeric(dept_inc[sev_col], errors="coerce")
                    
                    # Fatalities
                    fat_mask = pd.Series([False] * len(dept_inc))
                    if act_cons and act_cons in dept_inc.columns:
                        fat_mask |= dept_inc[act_cons].astype(str).str.contains("fatal", case=False, na=False)
                    if worst_cons and worst_cons in dept_inc.columns:
                        fat_mask |= dept_inc[worst_cons].astype(str).str.contains("fatal", case=False, na=False)
                    max_val = sev_vals.max(skipna=True)
                    if pd.notna(max_val):
                        thr = 5 if max_val >= 5 else 4
                        fat_mask |= sev_vals >= thr
                    fatalities = int(fat_mask.sum())
                    
                    # Lost Workday Cases
                    lti_mask = (sev_vals >= 3) & ~fat_mask
                    lost_workday = int(lti_mask.sum())
                    
                    # Recordable Injuries
                    rec_mask = (sev_vals >= 2) & ~(lti_mask | fat_mask)
                    recordable = int(rec_mask.sum())
                
                # Near misses from incidents
                near_miss_inc = 0
                if type_col and type_col in dept_inc.columns:
                    near_miss_inc = int(dept_inc[type_col].astype(str).str.contains("near miss|near-miss", case=False, na=False).sum())
                
                # Near misses from hazards
                near_miss_haz = 0
                if haz_df is not None and not haz_df.empty:
                    haz_dept_col = _resolve_column(haz_df, ["department", "sub_department"])
                    if haz_dept_col and haz_dept_col in haz_df.columns:
                        near_miss_haz = int((haz_df[haz_dept_col] == dept).sum())
                
                # At-risk behaviors from audits
                at_risk_aud = 0
                if aud_df is not None and not aud_df.empty:
                    aud_loc_col = _resolve_column(aud_df, ["finding_location", "location", "audit_location"])
                    if aud_loc_col and aud_loc_col in aud_df.columns:
                        at_risk_aud = int(aud_df[aud_loc_col].astype(str).str.contains(str(dept), case=False, na=False).sum())
                
                # At-risk behaviors from inspections
                at_risk_insp = 0
                if insp_df is not None and not insp_df.empty:
                    insp_loc_col = _resolve_column(insp_df, ["finding_location", "location", "audit_location"])
                    if insp_loc_col and insp_loc_col in insp_df.columns:
                        at_risk_insp = int(insp_df[insp_loc_col].astype(str).str.contains(str(dept), case=False, na=False).sum())
                
                breakdown["by_department"].append({
                    "department": str(dept),
                    "fatalities": fatalities,
                    "lost_workday_cases": lost_workday,
                    "recordable_injuries": recordable,
                    "near_misses": near_miss_inc + near_miss_haz,
                    "at_risk_behaviors": at_risk_aud + at_risk_insp,
                    "total_incidents": int(len(dept_inc))
                })
    
    # Location breakdown
    if inc_df is not None and not inc_df.empty:
        loc_col = _resolve_column(inc_df, ["location", "sublocation", "location.1"])
        
        if loc_col and loc_col in inc_df.columns:
            for loc in inc_df[loc_col].dropna().unique():
                loc_inc = inc_df[inc_df[loc_col] == loc]
                
                # Calculate layers for this location
                fatalities = 0
                lost_workday = 0
                recordable = 0
                
                if sev_col and sev_col in loc_inc.columns:
                    sev_vals = pd.to_numeric(loc_inc[sev_col], errors="coerce")
                    
                    # Fatalities
                    fat_mask = pd.Series([False] * len(loc_inc))
                    if act_cons and act_cons in loc_inc.columns:
                        fat_mask |= loc_inc[act_cons].astype(str).str.contains("fatal", case=False, na=False)
                    if worst_cons and worst_cons in loc_inc.columns:
                        fat_mask |= loc_inc[worst_cons].astype(str).str.contains("fatal", case=False, na=False)
                    max_val = sev_vals.max(skipna=True)
                    if pd.notna(max_val):
                        thr = 5 if max_val >= 5 else 4
                        fat_mask |= sev_vals >= thr
                    fatalities = int(fat_mask.sum())
                    
                    # Lost Workday Cases
                    lti_mask = (sev_vals >= 3) & ~fat_mask
                    lost_workday = int(lti_mask.sum())
                    
                    # Recordable Injuries
                    rec_mask = (sev_vals >= 2) & ~(lti_mask | fat_mask)
                    recordable = int(rec_mask.sum())
                
                # Near misses from incidents
                near_miss_inc = 0
                if type_col and type_col in loc_inc.columns:
                    near_miss_inc = int(loc_inc[type_col].astype(str).str.contains("near miss|near-miss", case=False, na=False).sum())
                
                # Near misses from hazards
                near_miss_haz = 0
                if haz_df is not None and not haz_df.empty:
                    haz_loc_col = _resolve_column(haz_df, ["location", "sublocation", "location.1"])
                    if haz_loc_col and haz_loc_col in haz_df.columns:
                        near_miss_haz = int((haz_df[haz_loc_col] == loc).sum())
                
                # At-risk behaviors from audits
                at_risk_aud = 0
                if aud_df is not None and not aud_df.empty:
                    aud_loc_col = _resolve_column(aud_df, ["location", "finding_location", "audit_location"])
                    if aud_loc_col and aud_loc_col in aud_df.columns:
                        at_risk_aud = int((aud_df[aud_loc_col] == loc).sum())
                
                # At-risk behaviors from inspections
                at_risk_insp = 0
                if insp_df is not None and not insp_df.empty:
                    insp_loc_col = _resolve_column(insp_df, ["location", "finding_location", "audit_location"])
                    if insp_loc_col and insp_loc_col in insp_df.columns:
                        at_risk_insp = int((insp_df[insp_loc_col] == loc).sum())
                
                breakdown["by_location"].append({
                    "location": str(loc),
                    "fatalities": fatalities,
                    "lost_workday_cases": lost_workday,
                    "recordable_injuries": recordable,
                    "near_misses": near_miss_inc + near_miss_haz,
                    "at_risk_behaviors": at_risk_aud + at_risk_insp,
                    "total_incidents": int(len(loc_inc))
                })
    
    return JSONResponse(content=to_native_json(breakdown))


# ======================= SITE SAFETY INDEX =======================

@router.get("/site-safety-index")
async def site_safety_index(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2024-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
    location: Optional[str] = Query(None, description="Filter by location", example="Manufacturing Facility"),
):
    """
    Site Safety Index (0-100 score) - Real-time safety health indicator.
    
    Calculation methodology:
    - Base score: 100
    - Deductions:
      - Serious injuries: -10 points each
      - Minor injuries: -3 points each
      - Hazards (high risk): -2 points each
      - Open corrective actions: -1 point each
    - Bonuses:
      - Days since last incident: +0.1 per day (max +10)
      - Completed audits: +0.5 each (max +5)
    """
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    aud_df = get_audit_df()
    
    # Apply filters
    inc_df = _apply_filters(inc_df, start_date, end_date, location)
    haz_df = _apply_filters(haz_df, start_date, end_date, location)
    
    base_score = 100.0
    deductions = 0.0
    bonuses = 0.0
    breakdown = []
    
    # Deductions from incidents
    if inc_df is not None and not inc_df.empty:
        sev_score_col = _resolve_column(inc_df, ["severity_score", "risk_score"])
        sev_text_col = _resolve_column(inc_df, ["actual_consequence_incident", "severity"])
        
        serious_count = 0
        minor_count = 0
        
        for idx, row in inc_df.iterrows():
            sev_score = row[sev_score_col] if sev_score_col else None
            sev_text = row[sev_text_col] if sev_text_col else None
            level = _classify_severity_level(sev_score, sev_text)
            
            if level == "Serious Injury/Fatality":
                serious_count += 1
            elif level == "Minor Injury":
                minor_count += 1
        
        serious_deduction = serious_count * 10
        minor_deduction = minor_count * 3
        deductions += serious_deduction + minor_deduction
        
        if serious_count > 0:
            breakdown.append({"factor": f"Serious Injuries ({serious_count})", "impact": -serious_deduction})
        if minor_count > 0:
            breakdown.append({"factor": f"Minor Injuries ({minor_count})", "impact": -minor_deduction})
    
    # Deductions from high-risk hazards
    if haz_df is not None and not haz_df.empty:
        risk_col = _resolve_column(haz_df, ["risk_score", "risk_level"])
        if risk_col:
            high_risk = haz_df[risk_col].apply(
                lambda x: (pd.notna(x) and (
                    (isinstance(x, (int, float)) and x >= 3) or 
                    (isinstance(x, str) and any(k in str(x).lower() for k in ["high", "critical", "severe"]))
                ))
            ).sum()
            hazard_deduction = high_risk * 2
            deductions += hazard_deduction
            if high_risk > 0:
                breakdown.append({"factor": f"High-Risk Hazards ({high_risk})", "impact": -hazard_deduction})
    
    # Open corrective actions deduction
    if inc_df is not None and not inc_df.empty:
        status_col = _resolve_column(inc_df, ["status"])
        if status_col:
            open_count = inc_df[status_col].astype(str).str.contains(
                "open|pending|progress|review", case=False, na=False
            ).sum()
            open_deduction = open_count * 1
            deductions += open_deduction
            if open_count > 0:
                breakdown.append({"factor": f"Open Corrective Actions ({open_count})", "impact": -open_deduction})
    
    # Bonus: Days since last incident
    if inc_df is not None and not inc_df.empty:
        date_col = _resolve_column(inc_df, ["occurrence_date", "date"])
        if date_col:
            dates = pd.to_datetime(inc_df[date_col], errors="coerce")
            last_incident = dates.max()
            if pd.notna(last_incident):
                days_since = (pd.Timestamp.now() - last_incident).days
                days_bonus = min(days_since * 0.1, 10.0)
                bonuses += days_bonus
                breakdown.append({"factor": f"Days Since Last Incident ({days_since})", "impact": round(days_bonus, 2)})
    
    # Bonus: Completed audits
    if aud_df is not None and not aud_df.empty:
        status_col = _resolve_column(aud_df, ["audit_status", "status"])
        if status_col:
            completed = aud_df[status_col].astype(str).str.contains("closed|complete", case=False, na=False).sum()
            audit_bonus = min(completed * 0.5, 5.0)
            bonuses += audit_bonus
            if completed > 0:
                breakdown.append({"factor": f"Completed Audits ({completed})", "impact": round(audit_bonus, 2)})
    
    final_score = max(0.0, min(100.0, base_score - deductions + bonuses))
    
    # Determine rating
    if final_score >= 90:
        rating = "Excellent"
        color = "#4caf50"
    elif final_score >= 75:
        rating = "Good"
        color = "#8bc34a"
    elif final_score >= 60:
        rating = "Fair"
        color = "#ffc107"
    elif final_score >= 40:
        rating = "Poor"
        color = "#ff9800"
    else:
        rating = "Critical"
        color = "#f44336"
    
    return JSONResponse(content=to_native_json({
        "score": round(final_score, 2),
        "rating": rating,
        "color": color,
        "base_score": base_score,
        "total_deductions": round(deductions, 2),
        "total_bonuses": round(bonuses, 2),
        "breakdown": breakdown,
        "filters_applied": {
            "start_date": start_date,
            "end_date": end_date,
            "location": location,
        }
    }))


# ======================= KPI METRICS =======================

@router.get("/kpis/trir")
async def kpi_trir(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2023-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
    total_hours_worked: int = Query(2000000, description="Total hours worked (default: 2M for estimation)", example=2000000),
):
    """
    TRIR - Total Recordable Incident Rate
    Formula: (Number of recordable incidents × 200,000) / Total hours worked
    Industry benchmark: < 1.0 is excellent, < 3.0 is good
    """
    inc_df = get_incident_df()
    inc_df = _apply_filters(inc_df, start_date, end_date)
    
    if inc_df is None or inc_df.empty:
        recordable_count = 0
    else:
        # Recordable = severity >= 2 or medical treatment required
        sev_col = _resolve_column(inc_df, ["severity_score", "risk_score"])
        if sev_col:
            recordable_count = (pd.to_numeric(inc_df[sev_col], errors="coerce") >= 2).sum()
        else:
            recordable_count = len(inc_df)
    
    trir = (recordable_count * 200000) / total_hours_worked if total_hours_worked > 0 else 0
    
    # Benchmark assessment
    if trir < 1.0:
        benchmark = "Excellent"
        color = "#4caf50"
    elif trir < 3.0:
        benchmark = "Good"
        color = "#8bc34a"
    elif trir < 5.0:
        benchmark = "Average"
        color = "#ffc107"
    else:
        benchmark = "Needs Improvement"
        color = "#f44336"
    
    return JSONResponse(content=to_native_json({
        "value": round(trir, 2),
        "recordable_incidents": int(recordable_count),
        "total_hours_worked": total_hours_worked,
        "benchmark": benchmark,
        "color": color,
        "industry_standard": "< 1.0 Excellent, < 3.0 Good, < 5.0 Average",
    }))


@router.get("/kpis/ltir")
async def kpi_ltir(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2023-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
    total_hours_worked: int = Query(2000000, description="Total hours worked", example=2000000),
):
    """
    LTIR - Lost Time Incident Rate
    Formula: (Number of lost-time incidents × 200,000) / Total hours worked
    """
    inc_df = get_incident_df()
    inc_df = _apply_filters(inc_df, start_date, end_date)
    
    if inc_df is None or inc_df.empty:
        lost_time_count = 0
    else:
        # Lost time = severity >= 3
        sev_col = _resolve_column(inc_df, ["severity_score", "risk_score"])
        if sev_col:
            lost_time_count = (pd.to_numeric(inc_df[sev_col], errors="coerce") >= 3).sum()
        else:
            lost_time_count = 0
    
    ltir = (lost_time_count * 200000) / total_hours_worked if total_hours_worked > 0 else 0
    
    return JSONResponse(content=to_native_json({
        "value": round(ltir, 2),
        "lost_time_incidents": int(lost_time_count),
        "total_hours_worked": total_hours_worked,
    }))


@router.get("/kpis/pstir")
async def kpi_pstir(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2023-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
    total_hours_worked: int = Query(2000000, description="Total hours worked", example=2000000),
):
    """
    PSTIR - Process Safety Total Incident Rate
    Formula: (Number of PSM incidents × 200,000) / Total hours worked
    """
    inc_df = get_incident_df()
    inc_df = _apply_filters(inc_df, start_date, end_date)
    
    if inc_df is None or inc_df.empty:
        psm_count = 0
    else:
        # PSM incidents
        psm_col = _resolve_column(inc_df, ["psm", "pse_category"])
        if psm_col:
            psm_count = inc_df[psm_col].notna().sum()
        else:
            psm_count = 0
    
    pstir = (psm_count * 200000) / total_hours_worked if total_hours_worked > 0 else 0
    
    return JSONResponse(content=to_native_json({
        "value": round(pstir, 2),
        "psm_incidents": int(psm_count),
        "total_hours_worked": total_hours_worked,
    }))


@router.get("/kpis/near-miss-ratio")
async def kpi_near_miss_ratio(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2023-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
):
    """
    Near-Miss to Incident Ratio
    Industry benchmark: 10:1 (10 near-misses per incident indicates good reporting culture)
    """
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    
    inc_df = _apply_filters(inc_df, start_date, end_date)
    haz_df = _apply_filters(haz_df, start_date, end_date)
    
    ratio = _calculate_near_miss_ratio(inc_df, haz_df)
    
    incident_count = len(inc_df) if inc_df is not None else 0
    near_miss_count = len(haz_df) if haz_df is not None else 0
    
    # Benchmark
    if ratio >= 10:
        benchmark = "Excellent reporting culture"
        color = "#4caf50"
    elif ratio >= 5:
        benchmark = "Good"
        color = "#8bc34a"
    elif ratio >= 2:
        benchmark = "Fair"
        color = "#ffc107"
    else:
        benchmark = "Under-reporting likely"
        color = "#f44336"
    
    return JSONResponse(content=to_native_json({
        "ratio": ratio,
        "near_misses": int(near_miss_count),
        "incidents": int(incident_count),
        "benchmark": benchmark,
        "color": color,
        "industry_standard": "10:1 indicates healthy reporting culture",
    }))


@router.get("/kpis/summary")
async def kpis_summary(
    start_date: Optional[str] = Query(None, description="Filter start date", example="2023-01-01"),
    end_date: Optional[str] = Query(None, description="Filter end date", example="2024-12-31"),
):
    """Unified dashboard KPI summary with all critical metrics."""
    # Call individual KPI endpoints with proper parameters
    trir_resp = await kpi_trir(start_date, end_date, total_hours_worked=2000000)
    ltir_resp = await kpi_ltir(start_date, end_date, total_hours_worked=2000000)
    pstir_resp = await kpi_pstir(start_date, end_date, total_hours_worked=2000000)
    nmr_resp = await kpi_near_miss_ratio(start_date, end_date)
    safety_index_resp = await site_safety_index(start_date, end_date, location=None)
    
    # Extract JSON data from responses
    import json
    
    return JSONResponse(content=to_native_json({
        "trir": json.loads(trir_resp.body.decode()) if hasattr(trir_resp, 'body') else {},
        "ltir": json.loads(ltir_resp.body.decode()) if hasattr(ltir_resp, 'body') else {},
        "pstir": json.loads(pstir_resp.body.decode()) if hasattr(pstir_resp, 'body') else {},
        "near_miss_ratio": json.loads(nmr_resp.body.decode()) if hasattr(nmr_resp, 'body') else {},
        "safety_index": json.loads(safety_index_resp.body.decode()) if hasattr(safety_index_resp, 'body') else {},
    }))


# ======================= RISK ASSESSMENT ANALYTICS =======================

@router.get("/actual-risk-score")
async def actual_risk_score():
    """
    Actual Risk Score by Department
    
    Calculates risk scores based on actual injury consequences:
    - Filters incidents where Incident Type(s) == 'injury'
    - Maps Actual Consequence to severity scores (C0=1, C1=2, C2=3, C3=4, C4-C5=5)
    - Calculates likelihood based on injury count quintiles (1-5 scale)
    - Risk Score = Sum(Actual Severity) × Likelihood
    - Normalized Score = min-max normalization
    
    Returns department-level actual risk assessment sorted by risk score.
    """
    sheets = load_default_sheets()
    incident_df = sheets.get('Incident')
    
    if incident_df is None or incident_df.empty:
        return JSONResponse(content=to_native_json([]))
    
    # Strip column names
    incident_df.columns = incident_df.columns.str.strip()
    
    # Filter for injury incidents
    incidents_df = incident_df[
        incident_df['Incident Number'].notna() & 
        incident_df['Incident Type(s)'].notna() & 
        (incident_df['Incident Type(s)'].str.strip().str.lower() == 'injury')
    ].copy()
    
    if incidents_df.empty:
        return JSONResponse(content=to_native_json([]))
    
    # Severity scoring map
    severity_scores = {
        'C0 - No Ill Effect': 1,
        'C1 - Minor': 2,
        'C2 - Serious': 3,
        'C3 - Severe': 4,
        'C4 - Major': 5,
        'C5 - Catastrophic': 5
    }
    
    # Map actual severity to scores
    incidents_df['Actual_Severity'] = incidents_df['Actual Consequence (Incident)'].map(severity_scores).fillna(0)
    
    # Calculate injury counts per department
    injury_counts = incidents_df.groupby('Department').size().reset_index(name='Injury_Count')
    
    # Calculate likelihood based on quintiles
    if len(injury_counts) > 1:
        quantiles = injury_counts['Injury_Count'].quantile([0.2, 0.4, 0.6, 0.8]).values
    else:
        quantiles = [1, 1, 1, 1]
    
    def assign_likelihood(count):
        if count <= quantiles[0]: return 1
        elif count <= quantiles[1]: return 2
        elif count <= quantiles[2]: return 3
        elif count <= quantiles[3]: return 4
        else: return 5
    
    injury_counts['Likelihood'] = injury_counts['Injury_Count'].apply(assign_likelihood)
    
    # Aggregate by department
    dept_summary = incidents_df.groupby('Department').agg(
        Injury_Count=('Incident Number', 'count'),
        Sum_Actual_Severity=('Actual_Severity', 'sum')
    ).reset_index()
    
    # Merge with likelihood
    dept_summary = dept_summary.merge(injury_counts[['Department', 'Likelihood']], on='Department', how='left')
    
    # Calculate actual risk score
    dept_summary['Actual_Risk_Score'] = dept_summary['Sum_Actual_Severity'] * dept_summary['Likelihood']
    
    # Normalize scores
    min_score = dept_summary['Actual_Risk_Score'].min()
    max_score = dept_summary['Actual_Risk_Score'].max()
    if max_score != min_score:
        dept_summary['Normalized_Score'] = (
            (dept_summary['Actual_Risk_Score'] - min_score) / (max_score - min_score)
        )
    else:
        dept_summary['Normalized_Score'] = 0
    
    # Sort by risk score descending
    dept_summary = dept_summary.sort_values(by='Actual_Risk_Score', ascending=False)
    
    # Convert to records
    result = dept_summary[[
        'Department',
        'Likelihood',
        'Actual_Risk_Score',
        'Normalized_Score'
    ]].round(3).to_dict(orient='records')
    
    return JSONResponse(content=to_native_json(result))


@router.get("/potential-risk-score")
async def potential_risk_score():
    """
    Potential Risk Score by Department - Near-Miss Analysis
    
    Identifies and assesses near-miss incidents with high potential severity:
    - Filters incidents with minor actual consequence (C0/C1) but severe worst-case (C3-C5)
    - Maps Worst Case Consequence to severity scores
    - Calculates likelihood based on potential risk count quintiles
    - Risk Score = Sum(Worst Case Severity) × Likelihood
    - Normalized Score = min-max normalization
    
    This metric highlights departments with high-potential near-misses that could have resulted
    in serious incidents, helping prioritize proactive safety interventions.
    
    Returns department-level potential risk assessment sorted by risk score.
    """
    sheets = load_default_sheets()
    incident_df = sheets.get('Incident')
    
    if incident_df is None or incident_df.empty:
        return JSONResponse(content=to_native_json([]))
    
    # Strip column names
    incident_df.columns = incident_df.columns.str.strip()
    
    # Severity scoring map
    severity_scores = {
        'C0 - No Ill Effect': 1,
        'C1 - Minor': 2,
        'C2 - Serious': 3,
        'C3 - Severe': 4,
        'C4 - Major': 5,
        'C5 - Catastrophic': 5
    }
    
    # Filter for potential risk (near-miss) incidents
    potential_risk_df = incident_df[
        incident_df['Incident Number'].notna() &
        incident_df['Actual Consequence (Incident)'].notna() &
        incident_df['Worst Case Consequence (Incident)'].notna()
    ].copy()
    
    if potential_risk_df.empty:
        return JSONResponse(content=to_native_json([]))
    
    # Map severities
    potential_risk_df['Actual_Severity'] = potential_risk_df['Actual Consequence (Incident)'].map(severity_scores).fillna(0)
    potential_risk_df['Worst_Severity'] = potential_risk_df['Worst Case Consequence (Incident)'].map(severity_scores).fillna(0)
    
    # Filter for near-misses: minor actual (≤C1) but severe worst-case (≥C3)
    near_miss_df = potential_risk_df[
        (potential_risk_df['Actual_Severity'] <= 2) &
        (potential_risk_df['Worst_Severity'] >= 4)
    ].copy()
    
    if near_miss_df.empty:
        return JSONResponse(content=to_native_json([]))
    
    # Calculate potential risk counts per department
    potential_counts = near_miss_df.groupby('Department').size().reset_index(name='Potential_Risk_Count')
    
    # Calculate likelihood based on quintiles
    if len(potential_counts) > 1:
        pot_quantiles = potential_counts['Potential_Risk_Count'].quantile([0.2, 0.4, 0.6, 0.8]).values
    else:
        pot_quantiles = [1, 1, 1, 1]
    
    def assign_potential_likelihood(count):
        if count <= pot_quantiles[0]: return 1
        elif count <= pot_quantiles[1]: return 2
        elif count <= pot_quantiles[2]: return 3
        elif count <= pot_quantiles[3]: return 4
        else: return 5
    
    potential_counts['Potential_Likelihood'] = potential_counts['Potential_Risk_Count'].apply(assign_potential_likelihood)
    
    # Aggregate by department
    potential_summary = near_miss_df.groupby('Department').agg(
        Sum_Potential_Severity=('Worst_Severity', 'sum')
    ).reset_index()
    
    # Merge with likelihood
    potential_summary = potential_summary.merge(
        potential_counts[['Department', 'Potential_Likelihood']], 
        on='Department', 
        how='left'
    )
    
    # Calculate potential risk score
    potential_summary['Potential_Risk_Score'] = (
        potential_summary['Sum_Potential_Severity'] * potential_summary['Potential_Likelihood']
    )
    
    # Normalize scores
    min_pot = potential_summary['Potential_Risk_Score'].min()
    max_pot = potential_summary['Potential_Risk_Score'].max()
    if max_pot != min_pot:
        potential_summary['Normalized_Potential_Score'] = (
            (potential_summary['Potential_Risk_Score'] - min_pot) / (max_pot - min_pot)
        )
    else:
        potential_summary['Normalized_Potential_Score'] = 0
    
    # Sort by risk score descending
    potential_summary = potential_summary.sort_values(by='Potential_Risk_Score', ascending=False)
    
    # Convert to records
    result = potential_summary[[
        'Department',
        'Potential_Likelihood',
        'Potential_Risk_Score',
        'Normalized_Potential_Score'
    ]].round(3).to_dict(orient='records')
    
    return JSONResponse(content=to_native_json(result))
