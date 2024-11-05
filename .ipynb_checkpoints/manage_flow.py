from data_preprocessor_1 import drop_columns, change_column_type
from data_cleaning import get_date_columns, fill_missing_values
from data_preprocessor_2 import visualize_columns, handle_outliers, one_hot_encoding, bin_columns, handle_correlation
from model_and_evaluation import choose_feature_selection_method, supervised_model, evaluation_supervised, unsupervised_model, evaluation_unsupervised

def manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format):
    filled_df = df_date_format.copy()

    while True:
        print("\nChoose which stage you want to go:")
        print("1. Handle missing values")
        print("2. Change the format of date columns")
        print("3. Change data format again")
        print("4. Dropping columns")
        print("5. Continue")

        again = input("Select which action you want (1, 2, or 3): ").strip()

        if again == '1':
            filled_df = fill_missing_values(df_date_format) # Loop back to handle missing value again
            break  # Go back to handle missing value

        elif again == '2':
            # Go back to Change the format of date columns
            df_date_format = get_date_columns(df_type) # Change the format of date columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            return filled_df

        elif again == '3':
            # Go back to Change data format stage
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            return filled_df  # Return the modified DataFrame and continue

        elif again == '4':
            # Go back to drop columns stage
            df_drop = drop_columns(df)  # Drop columns and return the modified DataFrame
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            return filled_df  # Return the modified DataFrame and continue

        elif again == '5':
            # Proceed to next stage without further changes
            return filled_df  # Return the modified DataFrame and continue
        else:
            print("Invalid input. Please select 1, 2, 3, 4 or 5.")


def manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df, df_outlier):
    # df_outlier = filled_df.copy()

    while True:
        print("\nChoose which stage you want to go:")
        print("1. Calculate IQR and identify outliers and handle outliers")
        print("2. Handle missing values")
        print("3. Change the format of date columns")
        print("4. Change data format again")
        print("5. Dropping columns")
        print("6. Continue")

        again = input("Select which action you want (1, 2,..., 6): ").strip()

        if again == '1':
            df_outlier = handle_outliers(filled_df) # Loop back to calculate IQR and identify outliers and handle outliers
            break  # Go back to handling outlier

        elif again == '2':
            filled_df = fill_missing_values(df_date_format) # Loop back to handle missing value again
            # filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format)
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            return df_outlier # Go back to handle missing value

        elif again == '3':
            # Go back to Change the format of date columns
            df_date_format = get_date_columns(df_type) # Change the format of date columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            # filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format)
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            return df_outlier

        elif again == '4':
            # Go back to Change data format stage
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            # filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format)
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            return df_outlier  # Return the modified DataFrame and continue

        elif again == '5':
            # Go back to drop columns stage
            df_drop = drop_columns(df)  # Drop columns and return the modified DataFrame
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            # filled_df = manage_user_flow_missing_value_stage(df, df_drop, df_type, df_date_format)
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            return df_outlier  # Return the modified DataFrame and continue

        elif again == '6':
            # Proceed to next stage without further changes
            return df_outlier  # Return the modified DataFrame and continue
        else:
            print("Invalid input. Please select 1, 2, 3, 4 or 5.")

# Managing after binning and one-hot-encoding
def manage_user_flow_binning_one_hot_encoding(df, df_drop, df_type, df_date_format, filled_df, df_outlier
                                              , df_drop_two, df_bin, df_one_hot):
    # df_outlier = filled_df.copy()

    while True:
        print("\nChoose which stage you want to go:")
        print("1. One-hot encoding")
        print("2. Binning")
        print("3. Calculate IQR and identify outliers and handle outliers")
        print("4. Handle missing values")
        print("5. Change the format of date columns")
        print("6. Change data format again")
        print("7. Dropping columns")
        print("8. Continue")

        again = input("Select which action you want (1, 2, or 3): ").strip()

        if again == '1':
            df_one_hot = one_hot_encoding(df_bin) # Loop back to one-hot encoding
            break  # Go back to one-hot-encoding

        elif again == '2':
            df_bin = bin_columns(df_drop_two) # Loop back to binning
            df_one_hot = one_hot_encoding(df_bin)
            return df_one_hot  # Go back to binning encoding

        elif again == '3':
            df_outlier = handle_outliers(filled_df) # Loop back to calculate IQR and identify outliers and handle outliers
            # df_outlier = manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            return  df_one_hot # Go back to handling outlier

        elif again == '4':
            filled_df = fill_missing_values(df_date_format) # Loop back to handle missing value again
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            return  df_one_hot

        elif again == '5':
            # Go back to Change the format of date columns
            df_date_format = get_date_columns(df_type) # Change the format of date columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            return df_one_hot

        elif again == '6':
            # Go back to Change data format stage
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            return df_one_hot

        elif again == '7':
            # Go back to drop columns stage
            df_drop = drop_columns(df)  # Drop columns and return the modified DataFrame
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            return df_one_hot

        elif again == '8':
            # Proceed to next stage without further changes
            return df_one_hot  # Return the modified DataFrame and continue
        else:
            print("Invalid input. Please select 1, 2, 3, 4, 5, 6, 7 or 8.")

def manage_user_flow_model_and_evaluation(df, df_drop, df_type, df_date_format, filled_df, df_outlier
                                              , df_drop_two, df_bin, df_one_hot):

    while True:
        print("\nChoose which stage you want to go:")
        print("1. Supervised Learning and evaluation")
        print("2. Unsupervised Learning and evaluation")
        print("3. One-hot encoding")
        print("4. Binning")
        print("5. Calculate IQR and identify outliers and handle outliers")
        print("6. Handle missing values")
        print("7. Change the format of date columns")
        print("8. Change data format again")
        print("9. Dropping columns")
        print("10. Exit")

        again = input("Select which action you want (1, 2, or 3): ").strip()

        if again == '1':
            model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
            evaluation_supervised(model, X_test, y_test) # Loop back to supervised-learning
            break  # Go back to supervised-learning

        elif again == '2':
            model, labels, model_choice = unsupervised_model(df_one_hot)
            evaluation_unsupervised(df_one_hot, labels, model_choice) # Loop back to unsupervised-learning
            break  # Go back to unsupervised-learning

        elif again == '3':
            df_one_hot = one_hot_encoding(df_bin) # Loop back to one-hot encoding
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)
            continue  # Go back to

        elif again == '4':
            df_bin = bin_columns(df_drop_two) # Loop back to binning
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return df_one_hot  # Go back to binning encoding

        elif again == '5':
            df_outlier = handle_outliers(filled_df) # Loop back to calculate IQR and identify outliers and handle outliers
            # df_outlier = manage_user_flow_handle_outliers(df, df_drop, df_type, df_date_format, filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return  df_one_hot # Go back to handling outlier

        elif again == '6':
            filled_df = fill_missing_values(df_date_format) # Loop back to handle missing value again
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return  df_one_hot

        elif again == '7':
            # Go back to Change the format of date columns
            df_date_format = get_date_columns(df_type) # Change the format of date columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return df_one_hot

        elif again == '8':
            # Go back to Change data format stage
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return df_one_hot

        elif again == '9':
            # Go back to drop columns stage
            df_drop = drop_columns(df)  # Drop columns and return the modified DataFrame
            df_type = change_column_type(df_drop, df)  # Call change_column_type with the updated DataFrame
            df_date_format = get_date_columns(df_type) # Call get_date_columns
            filled_df = fill_missing_values(df_date_format) # Call fill_missing_values
            visualize_columns(filled_df)
            df_outlier = handle_outliers(filled_df)
            handle_correlation(df_outlier)
            df_drop_two = drop_columns(df_outlier)
            df_bin = bin_columns(df_drop_two)
            df_one_hot = one_hot_encoding(df_bin)
            method = choose_feature_selection_method()

            if method == 'supervised':
                model, X_test, y_test, X_train, y_train = supervised_model(df_one_hot)
                evaluation_supervised(model, X_test, y_test)

            else:
                model, labels, model_choice = unsupervised_model(df_one_hot)
                evaluation_unsupervised(df_one_hot, labels, model_choice)

            return df_one_hot

        elif again == '10':
            # Exit the program
            print("Exiting the workflow. Thank you!")
            break

        else:
            print("Invalid input. Please select 1, 2, 3, 4, 5, 6, 7, 8, 9 or 10.")

