import duckdb
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'entity_resolution.db')

def get_connection():
    """Returns a DuckDB connection to the local database file."""
    # Ensure the directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    con = duckdb.connect(DB_PATH)
    return con

def init_db():
    """Initializes the database schema if it doesn't exist."""
    con = get_connection()
    
    # Raw table for incoming CSV data
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_people (
            id VARCHAR,
            first_name VARCHAR,
            last_name VARCHAR,
            email VARCHAR,
            dob VARCHAR,
            ssn VARCHAR,
            phone_number VARCHAR,
            address VARCHAR
        )
    """)
    
    # Processed table (cleaned)
    con.execute("""
        CREATE TABLE IF NOT EXISTS processed_people (
            id VARCHAR,
            uniq_id VARCHAR, -- Generated ID to track lineage
            first_name_norm VARCHAR,
            last_name_norm VARCHAR,
            email_norm VARCHAR,
            dob_std DATE,
            ssn_clean VARCHAR,
            phone_clean VARCHAR,
            full_address_norm VARCHAR
        )
    """)
    
    con.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db()
