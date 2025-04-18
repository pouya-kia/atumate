from data_loader import load_data,create_s3_client,read_csv_from_s3
from data_preprocessor_1 import show_column_info, drop_column, change_column_type
from data_cleaning import get_date_columns, fill_missing_values
from manage_flow import manage_user_flow_missing_value_stage, manage_user_flow_handle_outliers \
    , manage_user_flow_binning_one_hot_encoding, manage_user_flow_model_and_evaluation, manage_user_flow_changing_format
from data_preprocessor_2 import visualize_columns, handle_outliers, handle_correlation, bin_columns \
    , one_hot_encoding # , drop_columns
from model_and_evaluation import choose_feature_selection_method, supervised_model, evaluation_supervised \
    , unsupervised_model, evaluation_unsupervised
import pandas as pd

def main():
    # Load the data
    object_name = input("Enter the data source (file path or database connection string): ")
    # source
    # df = load_data(source)

    # COMMENT: use url (csv)
    # Secret key work only 48h and after that change
    access_key = "t0VrBwOBGgBmgeOp"
    secret_key = "q3DR2Y6lBAhV3kW6uqUJ3ByRDqUqLaeh"
    endpoint_url = "https://c170077.parspack.net"
    bucket_name = "c170077"
    # object_name = "data.csv"

    # Create an S3 client
    s3_client = create_s3_client(access_key, secret_key, endpoint_url)

    # Load the CSV file as a DataFrame
    df = read_csv_from_s3(s3_client, bucket_name, object_name)
    # df = df.to_json(orient="records")

    # Show column info
    show_column_info(df)

    # Take a copy from original data
    df = pd.read_json(df)
    df_copy = df.copy()
    df_copy = df_copy.to_json(orient="records")

    # Drop columns if needed
    df_drop = drop_column(df_copy)

    # Change column types if needed
    df_type = change_column_type(df_drop, df)

    # Get date columns and their formats
    df_date_format = get_date_columns(df_type)

    # Managing Flow after changing format
    df_date_format = manage_user_flow_changing_format(df, df_drop, df_type, df_date_format)

    print(type(df), type(df_drop), type(df_type),type(df_date_format))

    # Fill missing values in the DataFrame
    filled_df = fill_missing_values(df_date_format)
    print(type(df), type(df_drop), type(df_type), type(df_date_format),type(filled_df))

    # Managing Flow after missing values
    filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format, filled_df)
    print(type(df), type(df_drop), type(df_type), type(df_date_format),type(filled_df))


    # Visualize boxplot and histogram
    visualize_columns(filled_df)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df))

    # Calculate IQR and identify outliers and handle outliers
    df_outlier = handle_outliers(filled_df)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier))

    # Managing Flow after handling outlier
    df_outlier = manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df, df_outlier)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier))

    # Visualize linear and non-linear correlation
    handle_correlation(df_outlier)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier))

    df_copy_1 = df_outlier.copy()
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier),type(df_copy_1))

    # Drop columns if needed 2
    df_drop_two = drop_column(df_copy_1)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier),
          type(df_copy_1),type(df_drop_two))

    # Bin columns
    df_bin = bin_columns(df_drop_two)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier),
          type(df_copy_1),type(df_drop_two),type(df_bin))

    # One-hot columns
    df_one_hot = one_hot_encoding(df_bin)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier),
          type(df_copy_1),type(df_drop_two),type(df_bin), type(df_one_hot))

    # Managing Flow after binning and one-hot-encoding
    df_one_hot = manage_user_flow_binning_one_hot_encoding(df, df_drop, df_type, df_date_format, filled_df, df_outlier
                                                           , df_drop_two, df_bin, df_one_hot)
    print(type(df), type(df_drop), type(df_type), type(df_date_format), type(filled_df), type(df_outlier),
          type(df_copy_1),type(df_drop_two),type(df_bin), type(df_one_hot))
    # -------------------------
    # # pd.read_json(df)
    # # df_copy.to_json(orient="records")
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

    # # pd.read_json(df)
    # # df_copy.to_json(orient="records")
if __name__ == "__main__":
    main()
