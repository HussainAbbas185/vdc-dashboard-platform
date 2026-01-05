import duckdb
import pandas as pd
import os

DB_PATH = os.path.join('data', 'entity_resolution.db')

def init_data():
    conn = duckdb.connect(DB_PATH)
    
    # Create Buildings Data
    buildings_data = {
        'building_id': [1, 2, 3, 4, 5],
        'university_name': ['Eastern Illinois University', 'Eastern Illinois University', 'UIUC', 'UIUC', 'Test Uni'],
        'city': ['Charleston', 'Charleston', 'Urbana', 'Champaign', 'Chicago'],
        'capacity': [100, 250, 500, 300, 150]
    }
    df_build = pd.DataFrame(buildings_data)
    
    conn.execute("CREATE OR REPLACE TABLE buildings AS SELECT * FROM df_build")
    print("Created 'buildings' table.")
    
    # Create Sales Data (Bonus)
    sales_data = {
                'date': pd.date_range(start='2024-01-01', periods=10),
                'product': ['Widget A', 'Widget B'] * 5,
                'amount': [100, 200, 150, 300, 120, 250, 180, 320, 140, 280]
            }
    df_sales = pd.DataFrame(sales_data)
    conn.execute("CREATE OR REPLACE TABLE sales AS SELECT * FROM df_sales")
    print("Created 'sales' table.")
    
    conn.close()

if __name__ == "__main__":
    init_data()
