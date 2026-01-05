from sqlalchemy import create_engine, text
import pandas as pd

def get_db_engine(db_type, host, port, user, password, db_name):
    """
    Creates a SQLAlchemy engine for the specified database.
    """
    if db_type == "PostgreSQL":
        url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    elif db_type == "MySQL":
        url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
    elif db_type == "SQL Server":
        # Requires pyodbc, simplifying for now or alerting user
        raise NotImplementedError("SQL Server requires pyodbc installed manually.")
    else:
        raise ValueError(f"Unsupported DB Type: {db_type}")
    
    return create_engine(url)

def fetch_data(engine, query):
    """
    Executes a SQL query and returns a Pandas DataFrame.
    """
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
