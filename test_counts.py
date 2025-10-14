"""
Test script to verify data counts from Excel file
"""
import pandas as pd
import sys
from pathlib import Path

# Add server directory to path
sys.path.insert(0, str(Path(__file__).parent / "server"))

from app.services.excel import (
    get_incident_df, get_hazard_df, get_audit_df, get_inspection_df,
    load_default_sheets
)

def count_unique_ids(df, id_col):
    """Count unique non-null values in ID column."""
    if df is None or df.empty:
        return 0
    if id_col not in df.columns:
        print(f"  WARNING: Column '{id_col}' not found in dataframe")
        print(f"  Available columns: {list(df.columns[:5])}...")
        return 0
    unique_count = int(df[id_col].dropna().nunique())
    total_non_null = int(df[id_col].notna().sum())
    print(f"  Column '{id_col}': {unique_count} unique IDs, {total_non_null} total non-null values")
    return unique_count

print("=" * 80)
print("TESTING DATA COUNTS FROM EXCEL")
print("=" * 80)

# Test primary datasets
print("\n1. INCIDENTS:")
inc_df = get_incident_df()
if inc_df is not None:
    print(f"  Total rows: {len(inc_df)}")
    incidents_count = count_unique_ids(inc_df, "Incident Number")
    print(f"  Final count: {incidents_count}")
else:
    print("  No data loaded")

print("\n2. HAZARDS:")
haz_df = get_hazard_df()
if haz_df is not None:
    print(f"  Total rows: {len(haz_df)}")
    hazards_count = count_unique_ids(haz_df, "Incident Number")
    print(f"  Final count: {hazards_count}")
else:
    print("  No data loaded")

print("\n3. AUDITS:")
aud_df = get_audit_df()
if aud_df is not None:
    print(f"  Total rows: {len(aud_df)}")
    audits_count = count_unique_ids(aud_df, "Audit Number")
    print(f"  Final count: {audits_count}")
else:
    print("  No data loaded")

print("\n4. INSPECTIONS:")
insp_df = get_inspection_df()
if insp_df is not None:
    print(f"  Total rows: {len(insp_df)}")
    inspections_count = count_unique_ids(insp_df, "Audit Number")
    print(f"  Final count: {inspections_count}")
else:
    print("  No data loaded")

# Test findings sheets
print("\n5. FINDINGS SHEETS:")
sheets = load_default_sheets()
print(f"  Available sheets: {list(sheets.keys())}")

# Find audit findings
audit_findings_sheets = [name for name in sheets.keys() if 'audit' in name.lower() and 'find' in name.lower()]
print(f"\n  Audit Findings candidates: {audit_findings_sheets}")
if audit_findings_sheets:
    for sheet_name in audit_findings_sheets:
        df = sheets[sheet_name]
        if df is not None:
            print(f"\n  Sheet: '{sheet_name}'")
            print(f"    Total rows: {len(df)}")
            aud_find_count = count_unique_ids(df, "Audit Number")
            print(f"    Final count: {aud_find_count}")

# Find inspection findings
inspection_findings_sheets = [name for name in sheets.keys() if 'inspection' in name.lower() and 'find' in name.lower()]
print(f"\n  Inspection Findings candidates: {inspection_findings_sheets}")
if inspection_findings_sheets:
    for sheet_name in inspection_findings_sheets:
        df = sheets[sheet_name]
        if df is not None:
            print(f"\n  Sheet: '{sheet_name}'")
            print(f"    Total rows: {len(df)}")
            insp_find_count = count_unique_ids(df, "Audit Number")
            print(f"    Final count: {insp_find_count}")

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Incidents: {incidents_count if 'incidents_count' in locals() else 'N/A'}")
print(f"Hazards: {hazards_count if 'hazards_count' in locals() else 'N/A'}")
print(f"Audits: {audits_count if 'audits_count' in locals() else 'N/A'}")
print(f"Inspections: {inspections_count if 'inspections_count' in locals() else 'N/A'}")
print(f"Audit Findings: {aud_find_count if 'aud_find_count' in locals() else 'N/A'}")
print(f"Inspection Findings: {insp_find_count if 'insp_find_count' in locals() else 'N/A'}")
print("=" * 80)
