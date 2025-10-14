import pandas as pd
import sqlite3
import openpyxl
from pathlib import Path


def excel_to_sqlite(excel_file, sqlite_file=None, if_exists='replace'):
    """
    Convert an Excel file with all sheets to SQLite database.
    
    Parameters:
    -----------
    excel_file : str
        Path to the Excel file (.xlsx, .xls)
    sqlite_file : str, optional
        Path to SQLite database file. If None, uses same name as Excel file
    if_exists : str, default 'replace'
        How to behave if table exists: 'fail', 'replace', 'append'
    
    Returns:
    --------
    dict : Summary of conversion with sheet names and row counts
    """
    
    # Set default SQLite filename if not provided
    if sqlite_file is None:
        sqlite_file = Path(excel_file).stem + '.db'
    
    # Read all sheets from Excel file
    excel_data = pd.read_excel(excel_file, sheet_name=None, engine='openpyxl')
    
    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_file)
    
    conversion_summary = {}
    
    try:
        # Iterate through each sheet
        for sheet_name, df in excel_data.items():
            # Clean sheet name for use as table name (replace spaces and special chars)
            table_name = sheet_name.replace(' ', '_').replace('-', '_')
            table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
            
            # Handle empty sheet names
            if not table_name:
                table_name = 'sheet_unnamed'
            
            # Write DataFrame to SQLite
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists=if_exists,
                index=False,
                dtype=None  # Let pandas infer data types
            )
            
            conversion_summary[sheet_name] = {
                'table_name': table_name,
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns)
            }
            
            print(f"✓ Converted sheet '{sheet_name}' to table '{table_name}' ({len(df)} rows, {len(df.columns)} columns)")
    
    finally:
        conn.close()
    
    print(f"\n✓ Successfully created SQLite database: {sqlite_file}")
    return conversion_summary


def verify_conversion(sqlite_file):
    """
    Verify the SQLite database by listing all tables and their info.
    
    Parameters:
    -----------
    sqlite_file : str
        Path to SQLite database file
    """
    conn = sqlite3.connect(sqlite_file)
    cursor = conn.cursor()
    
    # Get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print(f"\nDatabase: {sqlite_file}")
    print(f"Total tables: {len(tables)}\n")
    
    for table in tables:
        table_name = table[0]
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        print(f"Table: {table_name}")
        print(f"  Rows: {row_count}")
        print(f"  Columns: {len(columns)}")
        print(f"  Column names: {[col[1] for col in columns]}")
        print()
    
    conn.close()


# Example usage
if __name__ == "__main__":
    # Replace with your Excel file path
    excel_file = "EPCL_VEHS_Data_Processed.xlsx"
    
    # Convert Excel to SQLite
    summary = excel_to_sqlite(excel_file)
    
    # Verify the conversion
    sqlite_file = Path(excel_file).stem + '.db'
    verify_conversion(sqlite_file)
    
    # Print detailed summary
    print("\n" + "="*50)
    print("CONVERSION SUMMARY")
    print("="*50)
    for sheet, info in summary.items():
        print(f"\nSheet: {sheet}")
        print(f"  → Table: {info['table_name']}")
        print(f"  → Rows: {info['rows']}")
        print(f"  → Columns: {info['columns']}")
        print(f"  → Column names: {', '.join(info['column_names'])}")