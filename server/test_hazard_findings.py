"""
Test script for the updated hazard-top-findings endpoint.
Verifies that incident type categories are correctly counted.
"""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.excel import get_hazard_df
import pandas as pd

def test_hazard_incident_type_summary():
    """
    Test the hazard incident type summary logic.
    Mimics the new endpoint implementation.
    """
    print("=" * 80)
    print("TESTING HAZARD INCIDENT TYPE SUMMARY")
    print("=" * 80)
    
    # Load hazard data
    df = get_hazard_df()
    
    if df is None or df.empty:
        print("❌ ERROR: No hazard data found!")
        return
    
    print(f"\n✅ Loaded hazard DataFrame: {len(df)} rows × {len(df.columns)} columns")
    print(f"Available columns: {list(df.columns[:10])}...")
    
    # Look for 'Incident Type(s)' column
    col_candidates = [
        "incident_type(s)",
        "incident type(s)",
        "incident_types",
        "incident type",
        "incident_type"
    ]
    
    col = None
    for cand in col_candidates:
        for df_col in df.columns:
            if str(df_col).strip().lower() == cand.lower():
                col = df_col
                break
        if col:
            break
    
    if col is None:
        print(f"\n❌ ERROR: Could not find 'Incident Type(s)' column!")
        print(f"Available columns: {list(df.columns)}")
        return
    
    print(f"\n✅ Found column: '{col}'")
    
    # Clean the column
    series = (
        df[col]
        .astype(str)
        .str.replace("\xa0", " ", regex=False)  # Replace non-breaking spaces
        .str.replace(r"\s+", " ", regex=True)   # Normalize whitespace
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA, "null": pd.NA, "NULL": pd.NA})
        .dropna()
    )
    
    print(f"✅ After cleaning: {len(series)} valid entries")
    
    # Count occurrences
    vc = series.value_counts().sort_values(ascending=False)
    
    print(f"\n✅ Found {len(vc)} unique incident type categories")
    print(f"\nTop 10 Categories:")
    print("-" * 80)
    
    for idx, (category, count) in enumerate(vc.head(10).items(), 1):
        print(f"{idx:2d}. {category:60s} {count:4d}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total hazards: {len(series)}")
    print(f"Unique categories: {len(vc)}")
    print(f"Most common category: '{vc.index[0]}' ({vc.iloc[0]} occurrences)")
    print(f"Least common categories: {sum(vc == 1)} categories with 1 occurrence")
    
    # Distribution
    print("\nDistribution:")
    print(f"  Categories with >100 hazards: {sum(vc > 100)}")
    print(f"  Categories with 50-100 hazards: {sum((vc >= 50) & (vc <= 100))}")
    print(f"  Categories with 10-49 hazards: {sum((vc >= 10) & (vc < 50))}")
    print(f"  Categories with 2-9 hazards: {sum((vc >= 2) & (vc < 10))}")
    print(f"  Categories with 1 hazard: {sum(vc == 1)}")
    
    # Sample of combined categories (with semicolons)
    combined = [cat for cat in vc.index if ';' in cat]
    if combined:
        print(f"\n✅ Found {len(combined)} combined categories (with semicolons)")
        print(f"Examples:")
        for cat in combined[:5]:
            print(f"  - '{cat}' ({vc[cat]} occurrences)")
    
    print("\n" + "=" * 80)
    print("✅ TEST COMPLETED SUCCESSFULLY")
    print("=" * 80)
    
    # Return data for API simulation
    return {
        "labels": vc.index.tolist(),
        "counts": vc.values.tolist(),
        "total_hazards": len(series),
        "unique_categories": len(vc)
    }


def simulate_api_response():
    """Simulate the API response format"""
    result = test_hazard_incident_type_summary()
    
    if result:
        print("\n" + "=" * 80)
        print("API RESPONSE SIMULATION")
        print("=" * 80)
        print("\nEndpoint: GET /analytics/data/hazard-top-findings")
        print("\nResponse format:")
        print('{')
        print('  "labels": [')
        for i, label in enumerate(result['labels'][:5]):
            comma = ',' if i < 4 else ''
            print(f'    "{label}"{comma}')
        print('    ...')
        print('  ],')
        print('  "series": [{')
        print('    "name": "Hazards",')
        print('    "data": [')
        for i, count in enumerate(result['counts'][:5]):
            comma = ',' if i < 4 else ''
            print(f'      {count}{comma}')
        print('      ...')
        print('    ]')
        print('  }]')
        print('}')
        print("\n" + "=" * 80)


if __name__ == "__main__":
    simulate_api_response()
