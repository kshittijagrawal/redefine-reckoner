import sqlite3
import pandas as pd
from redefine_reckoner.config import DB_FILE

def get_database_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def load_full_data():
    """Load and cache the entire dataset from the database."""
    conn = get_database_connection()
    query = "SELECT * FROM ready_reckoner"
    return pd.read_sql_query(query, conn)

def save_to_database(df, table_name='filtered_data'):
    conn = get_database_connection()
    df.to_sql(table_name, conn, if_exists='replace', index=False)

def load_from_database(table_name='filtered_data'):
    conn = get_database_connection()
    try:
        df = pd.read_sql(f'SELECT * FROM {table_name}', conn)
        return df
    except:
        return None