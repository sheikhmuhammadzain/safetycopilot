"""
Filters Router - Corrected for actual dataset columns
Provides dropdown options for location, department, status, and other filter fields.
"""
from __future__ import annotations

from typing import List, Dict, Any, Optional
import pandas as pd
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..services.excel import get_incident_df, get_hazard_df, get_audit_df, get_inspection_df
from ..services.json_utils import to_native_json


router = APIRouter(prefix="/filters", tags=["filters"])


def _get_unique_values(df: pd.DataFrame, column_names: List[str]) -> List[str]:
    """
    Extract unique non-null values from specified columns.
    Returns combined unique values from all matching columns.
    """
    if df is None or df.empty:
        return []
    
    all_values = set()
    
    for column in column_names:
        if column in df.columns:
            values = df[column].dropna().astype(str).unique()
            # Filter out empty strings and common null-like values
            values = [
                v.strip() for v in values 
                if v and str(v).strip() and str(v).strip().lower() not in [
                    'nan', 'none', 'not specified', 'not assigned', 'n/a', 'na', ''
                ]
            ]
            all_values.update(values)
    
    return sorted(list(all_values))


@router.get("/locations")
async def get_locations():
    """
    Get all unique locations from all datasets for dropdown filters.
    
    Returns:
        List of unique location names sorted alphabetically
    """
    all_locations = set()
    
    # Incidents: Location, Sub-Location
    inc_df = get_incident_df()
    if inc_df is not None:
        locations = _get_unique_values(inc_df, ["Location", "Sub-Location", "Location (EPCL)"])
        all_locations.update(locations)
    
    # Hazards: Location, Sub-Location
    haz_df = get_hazard_df()
    if haz_df is not None:
        locations = _get_unique_values(haz_df, ["Location", "Sub-Location", "Location (EPCL)"])
        all_locations.update(locations)
    
    # Audits: Audit Location, Location (EPCL)
    aud_df = get_audit_df()
    if aud_df is not None:
        locations = _get_unique_values(aud_df, ["Audit Location", "Location (EPCL)"])
        all_locations.update(locations)
    
    # Inspections: Audit Location, Location (EPCL)
    insp_df = get_inspection_df()
    if insp_df is not None:
        locations = _get_unique_values(insp_df, ["Audit Location", "Location (EPCL)"])
        all_locations.update(locations)
    
    return JSONResponse(content=to_native_json({
        "locations": sorted(list(all_locations)),
        "count": len(all_locations)
    }))


@router.get("/departments")
async def get_departments():
    """
    Get all unique departments from all datasets for dropdown filters.
    
    Returns:
        List of unique department names sorted alphabetically
    """
    all_departments = set()
    
    # Incidents: Department, Sub-department, Section
    inc_df = get_incident_df()
    if inc_df is not None:
        departments = _get_unique_values(inc_df, ["Department", "Sub-department", "Section"])
        all_departments.update(departments)
    
    # Hazards: Department, Sub-department, Section
    haz_df = get_hazard_df()
    if haz_df is not None:
        departments = _get_unique_values(haz_df, ["Department", "Sub-department", "Section"])
        all_departments.update(departments)
    
    return JSONResponse(content=to_native_json({
        "departments": sorted(list(all_departments)),
        "count": len(all_departments)
    }))


@router.get("/statuses")
async def get_statuses():
    """
    Get all unique statuses from all datasets for dropdown filters.
    
    Returns:
        List of unique status values sorted alphabetically
    """
    all_statuses = set()
    
    # Incidents: Status
    inc_df = get_incident_df()
    if inc_df is not None:
        statuses = _get_unique_values(inc_df, ["Status"])
        all_statuses.update(statuses)
    
    # Hazards: Status
    haz_df = get_hazard_df()
    if haz_df is not None:
        statuses = _get_unique_values(haz_df, ["Status"])
        all_statuses.update(statuses)
    
    # Audits: Audit Status
    aud_df = get_audit_df()
    if aud_df is not None:
        statuses = _get_unique_values(aud_df, ["Audit Status"])
        all_statuses.update(statuses)
    
    # Inspections: Audit Status
    insp_df = get_inspection_df()
    if insp_df is not None:
        statuses = _get_unique_values(insp_df, ["Audit Status"])
        all_statuses.update(statuses)
    
    return JSONResponse(content=to_native_json({
        "statuses": sorted(list(all_statuses)),
        "count": len(all_statuses)
    }))


@router.get("/incident-types")
async def get_incident_types():
    """
    Get all unique incident types for dropdown filters.
    
    Returns:
        List of unique incident type values
    """
    inc_df = get_incident_df()
    # Column: "Incident Type(s)" with completeness 33.36%
    incident_types = _get_unique_values(inc_df, ["Incident Type(s)", "Category"])
    
    # Split by semicolon as values can be multiple (e.g., "Other; No Loss / No Injury")
    expanded_types = set()
    for type_str in incident_types:
        parts = [p.strip() for p in type_str.split(";")]
        expanded_types.update(parts)
    
    return JSONResponse(content=to_native_json({
        "incident_types": sorted(list(expanded_types)),
        "count": len(expanded_types)
    }))


@router.get("/violation-types")
async def get_violation_types():
    """
    Get all unique violation types from hazards for dropdown filters.
    
    Returns:
        List of unique violation type values
    """
    haz_df = get_hazard_df()
    # Column: "Violation Type (Hazard ID)" with completeness 76.55%
    violation_types = _get_unique_values(haz_df, ["Violation Type (Hazard ID)"])
    
    return JSONResponse(content=to_native_json({
        "violation_types": violation_types,
        "count": len(violation_types)
    }))


@router.get("/companies")
async def get_companies():
    """
    Get all unique companies for dropdown filters.
    
    Returns:
        List of unique company names
    """
    all_companies = set()
    
    # Incidents: Group Company (100% completeness)
    inc_df = get_incident_df()
    if inc_df is not None:
        companies = _get_unique_values(inc_df, ["Group Company"])
        all_companies.update(companies)
    
    # Hazards: Group Company
    haz_df = get_hazard_df()
    if haz_df is not None:
        companies = _get_unique_values(haz_df, ["Group Company"])
        all_companies.update(companies)
    
    # Audits: Group Company
    aud_df = get_audit_df()
    if aud_df is not None:
        companies = _get_unique_values(aud_df, ["Group Company"])
        all_companies.update(companies)
    
    # Inspections: Group Company
    insp_df = get_inspection_df()
    if insp_df is not None:
        companies = _get_unique_values(insp_df, ["Group Company"])
        all_companies.update(companies)
    
    return JSONResponse(content=to_native_json({
        "companies": sorted(list(all_companies)),
        "count": len(all_companies)
    }))


@router.get("/consequences")
async def get_consequences():
    """
    Get all unique consequence values for dropdown filters.
    
    Returns:
        List of unique consequence values
    """
    all_consequences = set()
    
    # Incidents: Multiple consequence columns
    inc_df = get_incident_df()
    if inc_df is not None:
        consequences = _get_unique_values(inc_df, [
            "Worst Case Consequence (Incident)",
            "Actual Consequence (Incident)",
            "Relevant Consequence (Incident)"
        ])
        all_consequences.update(consequences)
    
    # Hazards: Hazard consequence columns  
    haz_df = get_hazard_df()
    if haz_df is not None:
        consequences = _get_unique_values(haz_df, [
            "Worst Case Consequence Potential (Hazard ID)",
            "Relevant Consequence (Hazard ID)"
        ])
        all_consequences.update(consequences)
    
    return JSONResponse(content=to_native_json({
        "consequences": sorted(list(all_consequences)),
        "count": len(all_consequences)
    }))


@router.get("/psm-categories")
async def get_psm_categories():
    """
    Get all unique PSM (Process Safety Management) categories.
    
    Returns:
        List of unique PSM category values
    """
    inc_df = get_incident_df()
    # Column: "PSM" with 32.36% completeness
    psm_categories = _get_unique_values(inc_df, ["PSM"])
    
    return JSONResponse(content=to_native_json({
        "psm_categories": psm_categories,
        "count": len(psm_categories)
    }))


@router.get("/pse-categories")
async def get_pse_categories():
    """
    Get all unique PSE (Process Safety Event) categories.
    
    Returns:
        List of unique PSE category values
    """
    inc_df = get_incident_df()
    # Column: "PSE Category" with 14.18% completeness
    pse_categories = _get_unique_values(inc_df, ["PSE Category", "Tier 3 Description"])
    
    return JSONResponse(content=to_native_json({
        "pse_categories": pse_categories,
        "count": len(pse_categories)
    }))


@router.get("/audit-types")
async def get_audit_types():
    """
    Get all unique audit types for dropdown filters.
    
    Returns:
        List of unique audit type values
    """
    aud_df = get_audit_df()
    # Column: "Audit Type (EPCL)" with 99.89% completeness
    audit_types = _get_unique_values(aud_df, ["Audit Type (EPCL)", "Auditing Body"])
    
    return JSONResponse(content=to_native_json({
        "audit_types": audit_types,
        "count": len(audit_types)
    }))


@router.get("/investigation-types")
async def get_investigation_types():
    """
    Get all unique investigation types.
    
    Returns:
        List of unique investigation type values
    """
    inc_df = get_incident_df()
    # Column: "Investigation Type" with 33.36% completeness
    investigation_types = _get_unique_values(inc_df, ["Investigation Type"])
    
    return JSONResponse(content=to_native_json({
        "investigation_types": investigation_types,
        "count": len(investigation_types)
    }))


@router.get("/injury-classifications")
async def get_injury_classifications():
    """
    Get all unique injury classification values.
    
    Returns:
        List of unique injury classification values
    """
    inc_df = get_incident_df()
    # Column: "Injury Classification" with 2.81% completeness
    injury_classifications = _get_unique_values(inc_df, ["Injury Classification"])
    
    return JSONResponse(content=to_native_json({
        "injury_classifications": injury_classifications,
        "count": len(injury_classifications)
    }))


@router.get("/root-causes")
async def get_root_causes():
    """
    Get all unique root cause values.
    
    Returns:
        List of unique root cause values
    """
    inc_df = get_incident_df()
    # Column: "Root Cause" with 33.36% completeness
    root_causes = _get_unique_values(inc_df, ["Root Cause", "Key Factor", "Contributing Factor"])
    
    # Split by semicolon as values can be multiple
    expanded_causes = set()
    for cause_str in root_causes:
        parts = [p.strip() for p in cause_str.split(";")]
        expanded_causes.update(parts)
    
    return JSONResponse(content=to_native_json({
        "root_causes": sorted(list(expanded_causes)),
        "count": len(expanded_causes)
    }))


@router.get("/all-filters")
async def get_all_filters():
    """
    Get all filter options in a single call for efficiency.
    
    Returns:
        Dictionary containing all filter options
    """
    # Load all dataframes once
    inc_df = get_incident_df()
    haz_df = get_hazard_df()
    aud_df = get_audit_df()
    insp_df = get_inspection_df()
    
    # Locations
    all_locations = set()
    if inc_df is not None:
        all_locations.update(_get_unique_values(inc_df, ["Location", "Sub-Location", "Location (EPCL)"]))
    if haz_df is not None:
        all_locations.update(_get_unique_values(haz_df, ["Location", "Sub-Location", "Location (EPCL)"]))
    if aud_df is not None:
        all_locations.update(_get_unique_values(aud_df, ["Audit Location", "Location (EPCL)"]))
    if insp_df is not None:
        all_locations.update(_get_unique_values(insp_df, ["Audit Location", "Location (EPCL)"]))
    
    # Departments
    all_departments = set()
    if inc_df is not None:
        all_departments.update(_get_unique_values(inc_df, ["Department", "Sub-department", "Section"]))
    if haz_df is not None:
        all_departments.update(_get_unique_values(haz_df, ["Department", "Sub-department", "Section"]))
    
    # Statuses
    all_statuses = set()
    if inc_df is not None:
        all_statuses.update(_get_unique_values(inc_df, ["Status"]))
    if haz_df is not None:
        all_statuses.update(_get_unique_values(haz_df, ["Status"]))
    if aud_df is not None:
        all_statuses.update(_get_unique_values(aud_df, ["Audit Status"]))
    if insp_df is not None:
        all_statuses.update(_get_unique_values(insp_df, ["Audit Status"]))
    
    # Companies
    all_companies = set()
    for df in [inc_df, haz_df, aud_df, insp_df]:
        if df is not None:
            all_companies.update(_get_unique_values(df, ["Group Company"]))
    
    # Incident Types
    incident_types = set()
    if inc_df is not None:
        types = _get_unique_values(inc_df, ["Incident Type(s)"])
        for type_str in types:
            parts = [p.strip() for p in type_str.split(";")]
            incident_types.update(parts)
    
    # Violation Types
    violation_types = []
    if haz_df is not None:
        violation_types = _get_unique_values(haz_df, ["Violation Type (Hazard ID)"])
    
    # Consequences
    all_consequences = set()
    if inc_df is not None:
        all_consequences.update(_get_unique_values(inc_df, [
            "Worst Case Consequence (Incident)",
            "Actual Consequence (Incident)",
            "Relevant Consequence (Incident)"
        ]))
    if haz_df is not None:
        all_consequences.update(_get_unique_values(haz_df, [
            "Worst Case Consequence Potential (Hazard ID)",
            "Relevant Consequence (Hazard ID)"
        ]))
    
    return JSONResponse(content=to_native_json({
        "locations": sorted(list(all_locations)),
        "departments": sorted(list(all_departments)),
        "statuses": sorted(list(all_statuses)),
        "companies": sorted(list(all_companies)),
        "incident_types": sorted(list(incident_types)),
        "violation_types": sorted(violation_types),
        "consequences": sorted(list(all_consequences)),
        "counts": {
            "locations": len(all_locations),
            "departments": len(all_departments),
            "statuses": len(all_statuses),
            "companies": len(all_companies),
            "incident_types": len(incident_types),
            "violation_types": len(violation_types),
            "consequences": len(all_consequences)
        }
    }))
