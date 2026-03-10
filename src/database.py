
import duckdb
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'entity_resolution.db')

def get_connection(read_only=False):
    """
    Returns a DuckDB connection. 
    Uses read_only=True for dashboard elements to prevent 'File is already open' IO errors.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    # DuckDB on Windows often locks files; read_only allows concurrent dashboard access
    try:
        con = duckdb.connect(DB_PATH, read_only=read_only)
        return con
    except Exception as e:
        # Fallback if the database is genuinely locked or unavailable
        print(f"Connection Error: {e}")
        return duckdb.connect(":memory:")

def init_db():
    con = get_connection(read_only=False)
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_people (
            id VARCHAR, first_name VARCHAR, last_name VARCHAR, email VARCHAR,
            dob VARCHAR, ssn VARCHAR, phone_number VARCHAR, address VARCHAR
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS processed_people (
            id VARCHAR, uniq_id VARCHAR, first_name_norm VARCHAR, last_name_norm VARCHAR,
            email_norm VARCHAR, dob_std DATE, ssn_clean VARCHAR, phone_clean VARCHAR, full_address_norm VARCHAR
        )
    """)
    con.close()

def load_kpis():
    con = get_connection(read_only=True)
    try:
        tables = con.execute("SHOW TABLES").df()['name'].tolist()
        if 'processed_people' not in tables:
            return 0, 0, 0, None
            
        total_records = con.execute("SELECT COUNT(*) FROM processed_people").fetchone()[0]
        
        if 'entity_clusters' in tables:
            clustered_count = con.execute("SELECT COUNT(*) FROM entity_clusters").fetchone()[0]
            unique_clusters = con.execute("SELECT COUNT(DISTINCT cluster_id) FROM entity_clusters").fetchone()[0]
            non_clustered = total_records - clustered_count
            
            total_identities = non_clustered + unique_clusters
            duplicates_resolved = clustered_count - unique_clusters
            
            top_duplicates = con.execute("""
                SELECT cluster_id, COUNT(*) as count 
                FROM entity_clusters 
                GROUP BY cluster_id 
                ORDER BY count DESC 
                LIMIT 50
            """).df()
        else:
            total_identities = total_records
            duplicates_resolved = 0
            top_duplicates = None
            
        return total_records, total_identities, duplicates_resolved, top_duplicates
    except:
        return 0, 0, 0, None
    finally:
        con.close()
