import pandas as pd
from data_preprocessor_1 import drop_column, change_column_type

def get_date_columns(df_type, change_date_structure: bool, date_format_info: dict):
    df_type = pd.read_json(df_type)
    df_date_format = df_type.copy()
    messages = []

    if change_date_structure:
        for col, fmt in date_format_info.items():
            if col not in df_date_format.columns:
                messages.append(f"Column '{col}' does not exist in the DataFrame. Skipping...")
                continue
            try:
                df_date_format[col] = pd.to_datetime(df_date_format[col], format=fmt, errors='coerce')
                messages.append(f"Successfully converted column '{col}' to datetime format.")
            except Exception as e:
                messages.append(f"Error converting column '{col}': {e}")
    else:
        messages.append("No columns chosen for formatting.")

    return {
        "data": df_date_format.to_json(orient="records"),
        "messages": messages
    }


def fill_missing_values(df_date_format, methods: dict):
    df_date_format = pd.read_json(df_date_format)
    filled_df = df_date_format.copy()
    messages = []

    if not methods:
        messages.append("No missing value method provided. Returning original data.")
        return {
            "data": filled_df.to_json(orient="records"),
            "messages": messages
        }
    drop_selected = any(method == '6' for method in methods.values())

    if drop_selected:

        filled_df.dropna(axis=0, inplace=True)
        messages.append("Dropped rows with missing values.")
    for column, method_number in methods.items():
        if method_number == '6':
            continue

        if column not in filled_df.columns:
            messages.append(f"Column '{column}' not found in the DataFrame.")
            continue
        try:
            method = {
                '1': 'ffill',
                '2': 'bfill',
                '3': 'mean',
                '4': 'median',
                '5': 'mode'
            }.get(method_number, None)
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

            messages.append(f"Successfully filled missing values in column '{column}' using '{method}'.")
        except Exception as e:
            messages.append(f"Error filling missing values in column '{column}': {e}.")

    return {
        "data": filled_df.to_json(orient="records"),
        "messages": messages
    }
