import time
import pandas as pd
from src.generator import generate_record
from src.database import get_connection
import random

def stream_data(interval_seconds=2):
    """
    Simulates a stream of data arriving every 'interval_seconds'.
    Inserts data into 'raw_people' AND triggers a mini-ETL/match to show updates.
    NOTE: In a real system, matching might run in batch or micro-batch.
    Here we insert to DB so the dashboard can verify counts increasing.
    """
    print(f"Starting Stream Simulation... (Ctrl+C to stop)")
    print(f"Injecting 1 record every {interval_seconds} seconds...")
    
    con = get_connection()
    # We need to ensure table exists in case it was dropped
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_stream_buffer (
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
    con.close()

    try:
        while True:
            # Generate 1 record (sometimes a duplicate of a recent one? For now just new)
            # To make it interesting, let's keep a history of recent generated to dup against
            
            rec = generate_record()
            
            # Insert into Buffer Table (Simulating Kafka Topic / API endpoint)
            con = get_connection()
            
            # Using pandas for easy insert
            df = pd.DataFrame([rec])
            
            # We append to raw_people so it shows up in main count
            # But in a real arch, we'd have a separate ingestion table.
            # For this demo, let's append to 'raw_people' if it exists.
            
            # We need to handle the schema creation if raw_people was made from Excel (variable cols).
            # We'll force create/append if matches.
            try:
                con.execute("INSERT INTO raw_people SELECT * FROM df")
                
                # Also run a lightweight refresh of processed? 
                # Doing full ETL every second is heavy. 
                # Let's just INSERT. The Dashboard can have a "Refresh" button or auto-poll.
                print(f" [STREAM] Injected: {rec['first_name']} {rec['last_name']}")
                
            except Exception as e:
                print(f"Stream Insert Error (Schema mismatch?): {e}")
                
            con.close()
            time.sleep(interval_seconds)
            
    except KeyboardInterrupt:
        print("Stopping stream...")

if __name__ == "__main__":
    stream_data()
