import duckdb
import os
from src.database import get_connection

RAW_CSV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw', 'input_data.csv')

def run_etl(input_path=None):
    con = get_connection()
    
    if input_path is None:
        # Default to generated CSV if no path provided
        input_path = RAW_CSV_PATH
        
    print(f"Loading data from: {input_path}")
    
    # 1. Load Raw Data
    # We use CREATE OR REPLACE to adapt to the schema of the uploaded file
    # instead of forcing a fixed schemas at this stage.
    
    # Check file extension
    if input_path.endswith('.xlsx'):
        import pandas as pd
        df = pd.read_excel(input_path)
        # Convert all to string to prevent type issues during load
        df = df.astype(str)
        con.execute("CREATE OR REPLACE TABLE raw_people AS SELECT * FROM df")
        
    else:
        # Assume CSV
        con.execute(f"""
            CREATE OR REPLACE TABLE raw_people AS 
            SELECT * FROM read_csv_auto('{input_path}', header=True)
        """)
    
    count = con.execute("SELECT COUNT(*) FROM raw_people").fetchone()[0]
    print(f"Loaded {count} raw records.")


    # 2. Transform & Normalize
    print("Transforming data...")
    
    # We drop the old processed table and recreate it to ensure it matches current columns
    con.execute("DROP TABLE IF EXISTS processed_people")
    
    # Check for missing columns and add NULLs if needed for the transformation query to succeed
    existing_cols = [c[0] for c in con.execute("DESCRIBE raw_people").fetchall()]
    required_cols = ['id', 'first_name', 'last_name', 'email', 'dob', 'ssn', 'phone_number', 'address']
    
    # Simple validation/polyfill logic
    for col in required_cols:
        if col not in existing_cols:
            # print(f"Warning: Input missing '{col}', filling with NULL")
            con.execute(f"ALTER TABLE raw_people ADD COLUMN {col} VARCHAR DEFAULT NULL")
            
    # Now valid insert
    query = """
    CREATE TABLE processed_people AS
    SELECT 
        id,
        id as uniq_id, -- Initially, unique ID is just the record ID
        LOWER(TRIM(first_name)) as first_name_norm,
        LOWER(TRIM(last_name)) as last_name_norm,
        LOWER(TRIM(email)) as email_norm,
        try_cast(dob as DATE) as dob_std,
        regexp_replace(cast(ssn as VARCHAR), '[^0-9]', '', 'g') as ssn_clean,
        regexp_replace(cast(phone_number as VARCHAR), '[^0-9]', '', 'g') as phone_clean,
        LOWER(TRIM(address)) as full_address_norm
    FROM raw_people
    """
    
    con.execute(query)
    
    p_count = con.execute("SELECT COUNT(*) FROM processed_people").fetchone()[0]
    print(f"Processed {p_count} cleaned records.")
    
    con.close()

if __name__ == "__main__":
    run_etl()
