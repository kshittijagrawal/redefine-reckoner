import pandas as pd
import sqlite3
import os

# Get the project root directory
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def csv_to_db(csv_file, db_file):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    
    # Write the data to a SQLite table
    df.to_sql('ready_reckoner', conn, if_exists='replace', index=False)
    
    # Close the connection
    conn.close()
    
    print(f"Data from {csv_file} has been successfully imported to {db_file}")

if __name__ == "__main__":
    csv_file = os.path.join(PROJECT_ROOT, 'database', 'Ready Reckoner Feature X Vertical - Aug 2023  - Method Features.csv')
    db_file = os.path.join(PROJECT_ROOT, 'database', 'ready_reckoner.db')
    csv_to_db(csv_file, db_file)