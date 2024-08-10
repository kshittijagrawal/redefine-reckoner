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

def create_table(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS features (
            Method TEXT,
            Name_of_the_Feature TEXT,
            Availability TEXT,
            Checkout_Type TEXT,
            Vertical_Name TEXT,
            Implementation_Status TEXT
        );
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def populate_table(conn, df):
    try:
        df.to_sql('features', conn, if_exists='replace', index=False)
    except sqlite3.Error as e:
        print(f"Error populating table: {e}")

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

    # Create the table
    create_table(conn)

    # Populate the table with data
    populate_table(conn, df)

    print("Database population complete.")

if __name__ == "__main__":
    main()
