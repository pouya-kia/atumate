from data_loader import load_data
from data_preprocessor_1 import show_column_info, drop_columns, change_column_type
from data_cleaning import get_date_columns, fill_missing_values
from manage_flow import manage_user_flow_missing_value_stage, manage_user_flow_handle_outliers \
    , manage_user_flow_binning_one_hot_encoding
from data_preprocessor_2 import visualize_columns, handle_outliers, handle_correlation, drop_columns, bin_columns \
    , one_hot_encoding
from model_and_evaluation import choose_feature_selection_method, supervised_learning, unsupervised_learning

def main():
    # Load the data
    source = input("Enter the data source (file path or database connection string): ")
    df = load_data(source)

    # Show column info
    show_column_info(df)

    # Drop columns if needed
    df_drop = drop_columns(df)

    # Change column types if needed
    df_type = change_column_type(df_drop, df)

    # Get date columns and their formats
    df_date_format = get_date_columns(df_type)
    # print(f"Date Columns: {date_columns}, Formats: {date_formats}")

    # Fill missing values in the DataFrame
    filled_df = fill_missing_values(df_date_format)

    # Managing Flow after missing values
    filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format)

    # Visualize boxplot and histogram
    visualize_columns(filled_df)

    # Calculate IQR and identify outliers and handle outliers
    df_outlier = handle_outliers(filled_df)

    # Managing Flow after handling outlier
    df_outlier = manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df, df_outlier)

    # Visualize linear and non-linear correlation
    handle_correlation(df_outlier)

    # Drop columns if needed 2
    df_drop_two = drop_columns(df_outlier)

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
        supervised_learning(df)
    else:
        unsupervised_learning(df)


    # Optionally: print final dataframe or perform further processing
    print("Final DataFrame:")
    print(df_one_hot.head(2))


if __name__ == "__main__":
    main()
