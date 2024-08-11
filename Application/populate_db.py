import sqlite3
import pandas as pd
import os
import json

def create_connection(db_path):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables(conn):
    try:
        conn.execute('''
        CREATE TABLE IF NOT EXISTS reckoner (
            Method TEXT,
            Name_of_the_Feature TEXT,
            Availability TEXT,
            Standard TEXT,
            Custom TEXT,
            S2S TEXT,
            Lending TEXT,
            Ecommerce TEXT,
            Travel TEXT,
            Gaming TEXT,
            Investments TEXT,
            DMT TEXT,
            Insurance TEXT,
            OTT TEXT,
            Government TEXT,
            "Cross Borders - Export Flow" TEXT,
            "Cross Borders - Import Flow" TEXT
        )
        ''')
        
        conn.execute('''
        CREATE TABLE IF NOT EXISTS features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reckoner_id INTEGER,
            flags TEXT,
            description TEXT,
            FOREIGN KEY (reckoner_id) REFERENCES reckoner(id)
        )
        ''')
        
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def populate_reckoner_table(conn, df):
    try:
        df.to_sql('reckoner', conn, if_exists='replace', index=False)
        print("Table 'reckoner' populated successfully.")
    except sqlite3.Error as e:
        print(f"Error populating reckoner table: {e}")

def populate_features_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, Name_of_the_Feature, Availability FROM reckoner WHERE Availability = 'Feature Request'")
        feature_requests = cursor.fetchall()
        
        for reckoner_id, feature_name, availability in feature_requests:
            flags = json.dumps(["flag1", "flag2"])  # Example flags, you should replace with actual data
            description = f"Feature request for {feature_name}"
            cursor.execute('''
            INSERT INTO features (reckoner_id, flags, description)
            VALUES (?, ?, ?)
            ''', (reckoner_id, flags, description))
        
        conn.commit()
        print("Table 'features' populated successfully.")
    except sqlite3.Error as e:
        print(f"Error populating features table: {e}")

def add_id_to_reckoner(conn):
    try:
        # Create a new table with ID
        conn.execute('''
        CREATE TABLE reckoner_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Method TEXT,
            Name_of_the_Feature TEXT,
            Availability TEXT,
            Standard TEXT,
            Custom TEXT,
            S2S TEXT,
            Lending TEXT,
            Ecommerce TEXT,
            Travel TEXT,
            Gaming TEXT,
            Investments TEXT,
            DMT TEXT,
            Insurance TEXT,
            OTT TEXT,
            Government TEXT,
            "Cross Borders - Export Flow" TEXT,
            "Cross Borders - Import Flow" TEXT
        )
        ''')

        # Copy data from old table to new table
        conn.execute('''
        INSERT INTO reckoner_new (Method, Name_of_the_Feature, Availability, Standard, Custom, S2S, Lending, Ecommerce, Travel, Gaming, Investments, DMT, Insurance, OTT, Government, "Cross Borders - Export Flow", "Cross Borders - Import Flow")
        SELECT Method, "Name of the Feature", Availability, Standard, Custom, S2S, Lending, Ecommerce, Travel, Gaming, Investments, DMT, Insurance, OTT, Government, "Cross Borders - Export Flow", "Cross Borders - Import Flow" FROM reckoner
        ''')

        # Drop old table
        conn.execute('DROP TABLE reckoner')

        # Rename new table to reckoner
        conn.execute('ALTER TABLE reckoner_new RENAME TO reckoner')

        print("Added ID column to reckoner table successfully.")
    except sqlite3.Error as e:
        print(f"Error adding ID column to reckoner table: {e}")

def print_table_info(conn):
    for table in ['reckoner', 'features']:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        print(f"\n{table.capitalize()} table structure:")
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

    # Create tables
    create_tables(conn)

    # Populate the reckoner table with data from CSV
    populate_reckoner_table(conn, df)

    # Add ID column to reckoner table
    add_id_to_reckoner(conn)

    # Populate the features table
    populate_features_table(conn)

    # Print table information
    print_table_info(conn)

    conn.close()
    print("\nDatabase population complete.")

if __name__ == "__main__":
    main()