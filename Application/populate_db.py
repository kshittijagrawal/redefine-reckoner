import sqlite3
import pandas as pd
import os

def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def populate_table_from_csv(conn, df):
    try:
        df.to_sql('features', conn, if_exists='replace', index=False)
        print("Table 'features' created and populated successfully.")
    except sqlite3.Error as e:
        print(f"Error creating and populating table: {e}")

def print_table_info(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(features)")
    columns = cursor.fetchall()
    print("\nTable structure:")
    for column in columns:
        print(f"Column: {column[1]}, Type: {column[2]}")

def main():
    db_path = "data/redefine_reckoner.db"
    csv_file_path = "data/Ready Reckoner.csv"

    # Check if CSV file exists
    if not os.path.exists(csv_file_path):
        print(f"CSV file not found at path: {csv_file_path}")
        return

    # Read CSV file into DataFrame
    try:
        df = pd.read_csv(csv_file_path)
        print(f"CSV file read successfully. Columns: {', '.join(df.columns)}")
    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        return
    except pd.errors.EmptyDataError:
        print(f"File is empty: {csv_file_path}")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # Establish database connection
    conn = create_connection(db_path)
    if conn is None:
        return

    # Create and populate the table with data from CSV
    populate_table_from_csv(conn, df)

    # Print table information
    print_table_info(conn)

    conn.close()
    print("\nDatabase population complete.")

if __name__ == "__main__":
    main()