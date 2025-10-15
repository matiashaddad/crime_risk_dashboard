import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os

# Config
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_FILE_PATH = os.path.join(BASE_DIR, '..', 'db', 'risk_database.db')
# DATABASE_FILE = '../db/risk_database.db'
# CSV_FILE = 'data/world_crime_index_2023.csv'
CSV_FILE = os.path.join(BASE_DIR, '..', 'data', 'world_crime_index_2023.csv')
# SCHEMA_FILE = 'database_schema.sql'
SCHEMA_FILE_PATH = os.path.join(BASE_DIR, 'database_schema.sql')
TABLE_NAME = 'crime_data'

def create_database_schema(db_path, schema_path):
    # Create table from script
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        with open(schema_path, 'r') as f:
            sql_script = f.read()

        cursor.executescript(sql_script)
        conn.commit()
        print(f"Schema created in: {db_path}")
    except sqlite3.Error as e:
        print(f"Error - Failure at creating db schema {e}")
    finally:
        if conn:
            conn.close()

def load_data_to_sql(csv_path, db_url, table_name):
    # Load, cleand and save data from db
    try:
        # 1. Extract
        df = pd.read_csv(csv_path)

        # 2. Transform
        # Clean and standarize names of columns
        df.columns = df.columns.str.lower().str.replace(' ', '_')

        # Rename columns to match with schema
        df = df.rename(columns={
            'grid_3x3ranksort': 'rank',
            'text_formatcitysort': 'city',
            'text_formatcountrysort': 'country',
            'grid_3x3crime_indexsort': 'crime_index',
            'grid_3x3safety_indexsort': 'safety_index'
        })

        # Delete rows with empty values in key columns
        df.dropna(subset=['city', 'country', 'crime_index', 'safety_index'], inplace=True)

        # Convert to correct datatypes
        df['rank'] = pd.to_numeric(df['rank'], errors='coerce').astype('Int64')
        df['crime_index'] = pd.to_numeric(df['crime_index'], errors='coerce')
        df['safety_index'] = pd.to_numeric(df['safety_index'], errors='coerce')

        # 3. Load
        engine = create_engine(db_url)
        df.to_sql(table_name, engine, if_exists='replace', index=False)

        print(f"Data correctly loaded to '{table_name}' of SQLite.")
        print(f"Total loaded logs: {len(df)}")

    except FileNotFoundError:
        print(f"Error: CSV not found in {csv_path}")
    except Exception as e:
        print(f"An error occured during the ETL process: {e}")

if __name__ == "__main__":
    # SQLite connection url 'sqlite:///path/to/db'
    # Correct rooting - os.path
    # db_abs_path = os.path.abspath(DATABASE_FILE)
    # db_url = f"sqlite:///{db_abs_path}"
    db_url = f"sqlite:///{DATABASE_FILE_PATH}"

    # 1. Create schema
    # create_database_schema(db_abs_path, SCHEMA_FILE)
    create_database_schema(DATABASE_FILE_PATH, SCHEMA_FILE_PATH)

    # 2. Load data
    # load_data_to_sql(CSV_FILE, db_url, TABLE_NAME)
    load_data_to_sql(CSV_FILE, db_url, TABLE_NAME)
