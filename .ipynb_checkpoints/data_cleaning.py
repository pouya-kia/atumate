import pandas as pd
from data_preprocessor_1 import drop_column, change_column_type

def get_date_columns(df_type):
    df_date_format = df_type.copy()
    print("Do you want to change the format of date columns?")
    change_date_structure = input("Enter Yes or No: ").strip().lower()

    if change_date_structure == 'yes':
        print("Available columns: ", list(df_date_format.columns))
        date_columns = input("Enter the names of date columns separated by commas: ").strip().split(',')
        date_columns = [col.strip() for col in date_columns]

        date_formats = {}
        for col in date_columns:
            if col not in df_date_format.columns:
                print(f"Column '{col}' does not exist in the DataFrame. Skipping...")
                continue  # Skip non-existent columns

            print(f"Choose the format for date column '{col}':")
            print("1. YYYY-MM-DD")
            print("2. DD/MM/YYYY")
            print("3. MM-DD-YYYY")
            print("4. Custom (you will be prompted to enter the format)")
            choice = input("Enter the number corresponding to your choice: ").strip()

            if choice == '1':
                date_formats[col] = '%Y-%m-%d'
            elif choice == '2':
                date_formats[col] = '%d/%m/%Y'
            elif choice == '3':
                date_formats[col] = '%m-%d-%Y'
            elif choice == '4':
                custom_format = input(f"Enter the custom date format for column '{col}': ").strip()
                date_formats[col] = custom_format
            else:
                print("Invalid choice. Defaulting to YYYY-MM-DD.")
                date_formats[col] = '%Y-%m-%d'

            # Convert the column to datetime format
            try:
                df_date_format[col] = pd.to_datetime(df_date_format[col], format=date_formats[col], errors='coerce')
                print(f"Successfully converted column '{col}' to datetime format.")
            except Exception as e:
                print(f"Error converting column '{col}': {e}")

    else:
        print("No columns chosen for formatting.")

    return df_date_format


# Function to choose a method to fill missing values
def choose_fillna_method():
    print("Do you want to fill missing values? (yes/no)")
    fill_choice = input("Enter yes or no: ").strip().lower()

    if fill_choice == 'no':
        return None

    # Show methods
    print("Choose a method to handle missing values:")
    print("1. Forward Fill (ffill)")
    print("2. Backward Fill (bfill)")
    print("3. Mean")
    print("4. Median")
    print("5. Mode")
    print("6. Drop Rows (dropna)")

    methods = {}
    while True:
        user_input = input(
            "Enter the columns and methods in the format (col1, method_number). (col2, method_number) and etc. or type 'done' to finish: ")
        if user_input.lower() == 'done':
            break

        # Split the user input into individual column-method pairs
        pairs = user_input.split('.')
        for pair in pairs:
            try:
                # Strip spaces and parentheses
                pair = pair.strip().strip('()')
                col, method_number = pair.split(',')
                col = col.strip()
                method_number = method_number.strip()

                # Add to methods dictionary
                methods[col] = method_number
            except ValueError:
                print(f"Invalid input: {pair}. Please use the format (column, method_number).")

    return methods


# Function to fill missing values in the DataFrame
def fill_missing_values(df_date_format):
    filled_df = df_date_format.copy()

    methods = choose_fillna_method()

    if not methods:
        return filled_df  # No filling required

    # Check if the drop method was selected
    drop_selected = any(method == '6' for method in methods.values())

    if drop_selected:
        # Drop rows with missing values
        filled_df.dropna(axis=0, inplace=True)
        print("Dropped rows with missing values.")

    # Process other methods
    for column, method_number in methods.items():
        if method_number == '6':
            continue  # Skip processing for method 6 as it's already handled

        if column in filled_df.columns:
            try:
                method = {
                    '1': 'ffill',
                    '2': 'bfill',
                    '3': 'mean',
                    '4': 'median',
                    '5': 'mode'
                }.get(method_number, None)

                if method:
                    if method == 'ffill':
                        filled_df[column].fillna(method='ffill', inplace=True)
                    elif method == 'bfill':
                        filled_df[column].fillna(method='bfill', inplace=True)
                    elif method == 'mean':
                        filled_df[column].fillna(filled_df[column].mean(), inplace=True)
                    elif method == 'median':
                        filled_df[column].fillna(filled_df[column].median(), inplace=True)
                    elif method == 'mode':
                        filled_df[column].fillna(filled_df[column].mode()[0], inplace=True)

                    print(f"Successfully filled missing values in column '{column}' using '{method}'.")
                else:
                    print(f"Invalid method for column '{column}': {method_number}.")

            except Exception as e:
                print(f"Error filling missing values in column '{column}': {e}.")
        else:
            print(f"Column '{column}' not found in the DataFrame.")

            # Offer choices to go back to drop columns stage or continue

    return filled_df

