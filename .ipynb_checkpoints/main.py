from data_loader import load_data
from data_preprocessor_1 import show_column_info, drop_column, change_column_type
from data_cleaning import get_date_columns, fill_missing_values
from manage_flow import manage_user_flow_missing_value_stage, manage_user_flow_handle_outliers \
    , manage_user_flow_binning_one_hot_encoding, manage_user_flow_model_and_evaluation, manage_user_flow_changing_format
from data_preprocessor_2 import visualize_columns, handle_outliers, handle_correlation, bin_columns \
    , one_hot_encoding # , drop_columns
from model_and_evaluation import choose_feature_selection_method, supervised_model, evaluation_supervised \
    , unsupervised_model, evaluation_unsupervised
import boto3
from botocore.client import Config
from io import StringIO
import pandas as pd

# COMMENT: use url (csv)
access_key = "t0VrBwOBGgBmgeOp"
secret_key = "q3DR2Y6lBAhV3kW6uqUJ3ByRDqUqLaeh"
endpoint_url = "https://c170077.parspack.net"
bucket_name = "c170077"
object_name = "data.csv"

try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        endpoint_url=endpoint_url,
        config=Config(signature_version='s3v4')
    )

    response = s3.get_object(Bucket=bucket_name, Key=object_name)

    csv_content = response['Body'].read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_content))

    print("Data in CSV:")
    print(df.head())

except Exception as e:
    print(f"An error occurred: {e}")


def main():
    # Load the data
    source = input("Enter the data source (file path or database connection string): ")
    df = load_data(source)

    # Show column info
    show_column_info(df)

    # Take a copy from original data
    df_copy = df.copy()

    # Drop columns if needed
    df_drop = drop_column(df_copy)

    # Change column types if needed
    df_type = change_column_type(df_drop, df)

    # Get date columns and their formats
    df_date_format = get_date_columns(df_type)

    # Managing Flow after changing format
    df_date_format = manage_user_flow_changing_format(df, df_drop, df_type, df_date_format)

    # Fill missing values in the DataFrame
    filled_df = fill_missing_values(df_date_format)

    # Managing Flow after missing values
    filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format, filled_df)

    # Visualize boxplot and histogram
    visualize_columns(filled_df)

    # Calculate IQR and identify outliers and handle outliers
    df_outlier = handle_outliers(filled_df)

    # Managing Flow after handling outlier
    df_outlier = manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df, df_outlier)

    # Visualize linear and non-linear correlation
    handle_correlation(df_outlier)

    df_copy_1 = df_outlier.copy()

    # Drop columns if needed 2
    df_drop_two = drop_column(df_copy_1)

    # Bin columns
    df_bin = bin_columns(df_drop_two)

    # One-hot columns
    df_one_hot = one_hot_encoding(df_bin)

    # Managing Flow after binning and one-hot-encoding
    df_one_hot = manage_user_flow_binning_one_hot_encoding(df, df_drop, df_type, df_date_format, filled_df, df_outlier
                                                           , df_drop_two, df_bin, df_one_hot)

    # Choose model
    method = choose_feature_selection_method()

    if method == 'supervised':
        model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
        evaluation_supervised(model, X_test, y_test)

    else:
        model, labels, model_choice = unsupervised_model(df_one_hot)
        evaluation_unsupervised(df_one_hot, labels, model_choice)

    manage_user_flow_model_and_evaluation(df, df_drop, df_type, df_date_format, filled_df, df_outlier
                                          , df_drop_two, df_bin, df_one_hot)

    # Optionally: print final dataframe or perform further processing
    print("Workflow complete. Thank you!")


if __name__ == "__main__":
    main()
