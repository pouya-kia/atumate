import pandas as pd
import sqlalchemy
import re

# Function to detect source type
def detect_source_type(source):
    if re.search(r'\.csv$', source):
        return 'csv'
    elif re.search(r'\.xlsx?$', source):
        return 'excel'
    elif re.search(r'sqlite://|postgresql://|mysql://|oracle://', source):
        return 'sql'
    else:
        raise ValueError("Unknown source type. Please provide a valid source file or connection string.")

# Function to show correct input format based on the engine type
def get_engine_format():
    print("Supported SQL Engines:")
    print("1. SQLite: sqlite:///path_to_database.db")
    print("2. PostgreSQL: postgresql://username:password@localhost:5432/database_name")
    print("3. MySQL: mysql://username:password@localhost:3306/database_name")
    print("4. Oracle: oracle://username:password@localhost:1521/service_name")
    engine = input("Please provide the database connection string (as per formats above): ")
    return engine

# Function to load data from different sources
def load_data(source):
    source_type = detect_source_type(source)

    if source_type == 'csv':
        return pd.read_csv(source)
    elif source_type == 'excel':
        return pd.read_excel(source)
    elif source_type == 'sql':
        engine = get_engine_format()
        sql_query = input("Enter the SQL query to load data: ")
        engine = sqlalchemy.create_engine(engine)
        return pd.read_sql_query(sql_query, engine)
    else:
        raise ValueError("Invalid data source type.")
