import pandas as pd
import sqlalchemy
import re
import boto3
from botocore.client import Config
from io import StringIO

# AWS S3 Configuration
access_key = "t0VrBwOBGgBmgeOp"
secret_key = "q3DR2Y6lBAhV3kW6uqUJ3ByRDqUqLaeh"
endpoint_url = "https://c170077.parspack.net"
bucket_name = "c170077"

# S3 Client setup
def create_s3_client(access_key, secret_key, endpoint_url):
    """
    Create an S3 client.
    """
    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        config=Config(signature_version='s3v4')
    )


def read_csv_from_s3(s3_client, bucket_name, object_name):
    """
    Load a CSV file from S3 and return it as a Pandas DataFrame.
    """
    try:
        # Retrieve the file from the bucket
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        # Read the content of the file
        csv_content = response['Body'].read().decode('utf-8')
        # Parse the content as a Pandas DataFrame
        df = pd.read_csv(StringIO(csv_content))
        print("CSV file loaded successfully.")
        return df
    except s3_client.exceptions.NoSuchKey:
        print(f"The file '{object_name}' does not exist in the bucket '{bucket_name}'.")
    except Exception as e:
        print(f"An error occurred while loading the file: {e}")


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
