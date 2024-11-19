import pandas as pd

# Function to show column descriptions and types and percent of null values for every column
def show_column_info(df):
    df = pd.read_json(df)
    print("Column Descriptions and Data Types:")
    print(df.info())
    print("\nMissing values for each column:")
    print(df.isnull().sum())
    for col in df.columns:
        missing_percentage = ((df[col].isnull().sum()) / df.shape[0]) * 100
        print(f"Column: {col}")
        print(f"Missing: {missing_percentage:.2f}%")
    print("\n")


# Function to ask if the user wants to drop columns and handle dropping
def drop_column(df):
    df = pd.read_json(df)
    df_drop = df.copy()

    # Loop until a valid response ("yes" or "no") is provided
    while True:
        drop_choice = input("Do you want to drop any columns? (yes/no): ").strip().lower()
        if drop_choice in ['yes', 'no']:
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

    if drop_choice == 'yes':
        while True:
            columns_to_drop = input("Enter the column names you want to drop, separated by commas: ").strip().split(',')

            # Validate if columns exist in the dataframe
            invalid_columns = [col for col in columns_to_drop if col not in df_drop.columns]
            if invalid_columns:
                print(f"Invalid column names: {', '.join(invalid_columns)}. Please try again.")
            else:
                # Drop the valid columns
                df_drop.drop(columns=columns_to_drop, inplace=True)
                print(f"Dropped columns: {', '.join(columns_to_drop)}.")
                break
    else:
        print("No columns were dropped.")

    return df_drop.to_json(orient="records")


# Function to change data type of columns if needed
def change_column_type(df_drop, df):
    df_drop = pd.read_json(df_drop)
    df_type = df_drop.copy()  # Copy dataframe to preserve original

    all_correct = input("Are all the data types correct? (yes/no): ").strip().lower()

    if all_correct == 'yes':
        print("Proceeding with the current data types.")
        return df_type.to_json(orient="records")

    elif all_correct == 'no':
        while True:
            columns_to_change = input(
                "Which columns do you want to change the format for? (comma-separated, or type 'exit' to stop): ").strip().split(
                ',')
            columns_to_change = [col.strip() for col in columns_to_change]

            if 'exit' in columns_to_change:
                print("Exiting column type change.")
                return df_type  # Exit the loop if the user types 'exit'

            for col in columns_to_change:
                if col in df_drop.columns:
                    print(f"Current data type of '{col}': {df_drop[col].dtype}")
                    new_type = input(
                        f"What data type would you like to convert '{col}' to? (e.g., int, float, str, datetime): ").strip().lower()

                    # Apply the type change with error handling
                    try:
                        if new_type == 'datetime':
                            df_type[col] = pd.to_datetime(df_type[col], errors='coerce')  # Convert to datetime
                        else:
                            df_type[col] = df_type[col].astype(new_type)  # Convert to other types (int, float, str)
                        print(f"Successfully converted '{col}' to {new_type}.")
                    except Exception as e:
                        print(f"Error converting '{col}' to {new_type}: {e}")
                else:
                    print(f"Column '{col}' not found in the dataframe. Please try again.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

    return df_type.to_json(orient="records")  # Default return: proceed to the next stage with the current dataframe
