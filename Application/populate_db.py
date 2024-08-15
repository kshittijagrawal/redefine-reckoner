import sqlite3
import pandas as pd
import json
import os

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
        CREATE TABLE IF NOT EXISTS checkout_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkout TEXT UNIQUE
        )
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS vertical_names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vertical TEXT UNIQUE
        )
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS methods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            method TEXT UNIQUE
        )
        ''')

        conn.execute('''
        CREATE TABLE IF NOT EXISTS reckoner (
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

        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def populate_table_from_json(conn, table_name, json_file_path, column_name):
    try:
        if not os.path.exists(json_file_path):
            print(f"JSON file not found at path: {json_file_path}")
            return
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        items = data.get(column_name)
        if not items:
            print(f"No data found for {column_name} in {json_file_path}")
            return
        
        cursor = conn.cursor()

        cursor.execute(f"SELECT {column_name} FROM {table_name}")
        existing_items = {row[0] for row in cursor.fetchall()}

        items_to_delete = existing_items - set(items)
        items_to_insert = set(items) - existing_items

        if items_to_delete:
            cursor.executemany(f"DELETE FROM {table_name} WHERE {column_name} = ?", [(item,) for item in items_to_delete])

        if items_to_insert:
            cursor.executemany(f"INSERT OR IGNORE INTO {table_name} ({column_name}) VALUES (?)", [(item,) for item in items_to_insert])

        conn.commit()
        print(f"Table '{table_name}' populated successfully.")
    except Exception as e:
        print(f"Error populating '{table_name}' table: {e}")

def populate_reckoner_table(conn, df):
    try:
        df.rename(columns={'Name of the Feature': 'Name_of_the_Feature'}, inplace=True)
        df.to_sql('reckoner', conn, if_exists='replace', index=False)
        print("Table 'reckoner' populated successfully.")
    except sqlite3.Error as e:
        print(f"Error populating reckoner table: {e}")

def populate_features_table(conn):
    try:
        cursor = conn.cursor()
        
        # Drop the existing table if it exists
        cursor.execute('DROP TABLE IF EXISTS features')
        
        # Create the new features table
        cursor.execute('''
        CREATE TABLE features (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reckoner_id INTEGER,
            flags TEXT,
            description TEXT,
            FOREIGN KEY (reckoner_id) REFERENCES reckoner(id)
        )
        ''')

        # Fetch feature requests
        cursor.execute("SELECT id, Name_of_the_Feature FROM reckoner WHERE Availability = 'Feature Request'")
        feature_requests = cursor.fetchall()

        # Insert new feature flags
        for reckoner_id, feature_name in feature_requests:
            # Example flags and description; replace these with actual data
            flags = json.dumps(["flag1", "flag2"])
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
        # Drop the new table if it exists
        conn.execute('DROP TABLE IF EXISTS reckoner_new')

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
        SELECT Method, Name_of_the_Feature, Availability, Standard, Custom, S2S, Lending, Ecommerce, Travel, Gaming, Investments, DMT, Insurance, OTT, Government, "Cross Borders - Export Flow", "Cross Borders - Import Flow" FROM reckoner
        ''')

        # Drop old table
        conn.execute('DROP TABLE IF EXISTS reckoner')

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
    csv_file_path = "data/static_data/Ready Reckoner.csv"

    if not os.path.exists(csv_file_path):
        print(f"CSV file not found at path: {csv_file_path}")
        return

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

    conn = create_connection(db_path)
    if conn is None:
        return

    create_tables(conn)

    populate_table_from_json(conn, "checkout_types", "data/static_data/checkout_types.json", "checkout")
    populate_table_from_json(conn, "vertical_names", "data/static_data/vertical_names.json", "vertical")
    populate_table_from_json(conn, "methods", "data/static_data/methods.json", "method")

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
