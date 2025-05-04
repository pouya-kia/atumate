# # AWS S3 Configuration
# access_key = "t0VrBwOBGgBmgeOp"
# secret_key = "q3DR2Y6lBAhV3kW6uqUJ3ByRDqUqLaeh"
# endpoint_url = "https://c170077.parspack.net"
# bucket_name = "c170077"

# # S3 Client setup
# def create_s3_client(access_key, secret_key, endpoint_url):
#     """
#     Create an S3 client.
#     """
#     return boto3.client(
#         's3',
#         aws_access_key_id=access_key,
#         aws_secret_access_key=secret_key,
#         endpoint_url=endpoint_url,
#         config=Config(signature_version='s3v4')
#     )
import pandas as pd
import sqlalchemy
import re
import boto3
from botocore.client import Config
from io import StringIO

def create_s3_client(access_key, secret_key, endpoint_url):
    return boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        config=Config(signature_version='s3v4')
    )


def read_csv_from_s3(s3_client, bucket_name, object_name):
    messages = []
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        csv_content = response['Body'].read().decode('utf-8')
        df = pd.read_csv(StringIO(csv_content))
        messages.append("CSV file loaded successfully from S3.")
        return {
            "data": df.to_json(orient="records"),
            "messages": messages
        }
    except s3_client.exceptions.NoSuchKey:
        messages.append(f"The file '{object_name}' does not exist in the bucket '{bucket_name}'.")
    except Exception as e:
        messages.append(f"An error occurred while loading the file: {e}")
    return {
        "data": None,
        "messages": messages
    }


def detect_source_type(source):
    if re.search(r'\.csv$', source):
        return 'csv'
    elif re.search(r'\.xlsx?$', source):
        return 'excel'
    elif re.search(r'sqlite://|postgresql://|mysql://|oracle://', source):
        return 'sql'
    else:
        raise ValueError("Unknown source type. Please provide a valid source file or connection string.")


def load_data_from_source(source, query=None):
    messages = []
    source_type = detect_source_type(source)

    try:
        if source_type == 'csv':
            df = pd.read_csv(source)
            messages.append("CSV file loaded successfully.")
        elif source_type == 'excel':
            df = pd.read_excel(source)
            messages.append("Excel file loaded successfully.")
        elif source_type == 'sql':
            if not query:
                raise ValueError("SQL query is required for database loading.")
            engine = sqlalchemy.create_engine(source)
            df = pd.read_sql_query(query, engine)
            messages.append("Data loaded successfully from SQL database.")
        else:
            raise ValueError("Unsupported data source.")

        return {
            "data": df.to_json(orient="records"),
            "messages": messages
        }

    except Exception as e:
        messages.append(f"Failed to load data: {e}")
        return {
            "data": None,
            "messages": messages
        }
