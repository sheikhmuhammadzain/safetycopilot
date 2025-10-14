"""Test script for incident-top-findings with severity breakdown"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.excel import get_incident_df
import pandas as pd

def test_incident_severity():
    print("=" * 80)
    print("TESTING INCIDENT SEVERITY BREAKDOWN")
    print("=" * 80)
    
    df = get_incident_df()
    if df is None or df.empty:
        print("❌ No incident data found!")
        return
    
    print(f"\n✅ Loaded {len(df)} incident records")
    
    # Find columns
    incident_col = None
    for col in df.columns:
        if "incident" in str(col).lower() and "type" in str(col).lower():
            incident_col = col
            break
    
    severity_col = None
    for col in df.columns:
        if "consequence" in str(col).lower() or "severity" in str(col).lower():
            severity_col = col
            break
    
    if not incident_col or not severity_col:
        print(f"❌ Columns not found!")
        print(f"Incident col: {incident_col}")
        print(f"Severity col: {severity_col}")
        return
    
    print(f"✅ Incident column: '{incident_col}'")
    print(f"✅ Severity column: '{severity_col}'")
    
    # Clean data
    def clean(s):
        return (s.astype(str)
                .str.replace("\xa0", " ", regex=False)
                .str.strip()
                .str.replace(r"\s+", " ", regex=True)
                .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA}))
    
    df[incident_col] = clean(df[incident_col])
    df[severity_col] = clean(df[severity_col])
    df_clean = df.dropna(subset=[incident_col, severity_col])
    
    print(f"✅ After cleaning: {len(df_clean)} records")
    
    # Group small incidents
    min_count = 8
    counts = df_clean[incident_col].value_counts()
    main_incidents = counts[counts >= min_count].index
    
    df_filtered = df_clean[df_clean[incident_col].isin(main_incidents)].copy()
    
    if (counts < min_count).any():
        others_df = df_clean[~df_clean[incident_col].isin(main_incidents)].copy()
        if not others_df.empty:
            others_df[incident_col] = "Others"
            df_filtered = pd.concat([df_filtered, others_df], ignore_index=True)
    
    # Create crosstab
    severity_order = ["C0 - No Ill Effect", "C1 - Minor", "C2 - Serious", "C3 - Severe"]
    matrix = pd.crosstab(df_filtered[incident_col], df_filtered[severity_col])
    
    for sev in severity_order:
        if sev not in matrix.columns:
            matrix[sev] = 0
    
    matrix = matrix[severity_order]
    matrix["Total"] = matrix.sum(axis=1)
    matrix = matrix.sort_values("Total", ascending=False)
    
    print(f"\n✅ Found {len(matrix)} incident types")
    print(f"\nTop 5 Incident Types with Severity Breakdown:")
    print("-" * 80)
    print(f"{'Incident Type':<30} {'C0':>6} {'C1':>6} {'C2':>6} {'C3':>6} {'Total':>8}")
    print("-" * 80)
    
    for idx, row in matrix.head(5).iterrows():
        print(f"{idx:<30} {int(row['C0 - No Ill Effect']):>6} {int(row['C1 - Minor']):>6} "
              f"{int(row['C2 - Serious']):>6} {int(row['C3 - Severe']):>6} {int(row['Total']):>8}")
    
    print("\n" + "=" * 80)
    print(f"✅ TEST COMPLETED")
    print(f"Total records used: {len(df_filtered)}")
    print(f"Incident types with <{min_count} records grouped as 'Others'")
    print("=" * 80)

if __name__ == "__main__":
    test_incident_severity()
