import pandas as pd

# نمایش اطلاعات ستون‌ها (فقط پیام‌ها، بدون تغییر دیتا)
def show_column_info(df):
    df = pd.read_json(df)
    messages = []

    messages.append("Column Descriptions and Data Types:")
    messages.append(str(df.dtypes))

    messages.append("Missing values for each column:")
    null_info = df.isnull().sum()
    for col in df.columns:
        missing_percentage = (null_info[col] / df.shape[0]) * 100
        messages.append(f"Column: {col} - Missing: {missing_percentage:.2f}%")

    return {
        "messages": messages
    }


# حذف ستون‌ها
def drop_column(df, columns_to_drop: list):
    # df = pd.read_json(df)
    df = pd.DataFrame(df)
    df_drop = df.copy()
    messages = []

    invalid_columns = [col for col in columns_to_drop if col not in df.columns]
    if invalid_columns:
        messages.append(f"Invalid column names: {', '.join(invalid_columns)}. Skipped.")

    valid_columns = [col for col in columns_to_drop if col in df.columns]
    if valid_columns:
        df_drop.drop(columns=valid_columns, inplace=True)
        messages.append(f"Dropped columns: {', '.join(valid_columns)}.")
    else:
        messages.append("No valid columns to drop.")

    return {
        "data": df_drop.to_json(orient="records"),
        "messages": messages
    }

# تغییر نوع داده‌ی ستون‌ها
def change_column_type(df, type_map: dict):
    # df = pd.read_json(df)
    df = pd.DataFrame(df)
    df_type = df.copy()
    messages = []

    for col, new_type in type_map.items():
        if col not in df.columns:
            messages.append(f"Column '{col}' not found. Skipping...")
            continue
        try:
            if new_type.lower() == 'datetime':
                df_type[col] = pd.to_datetime(df_type[col], errors='coerce')
            else:
                df_type[col] = df_type[col].astype(new_type)
            messages.append(f"Successfully converted '{col}' to {new_type}.")
        except Exception as e:
            messages.append(f"Error converting '{col}' to {new_type}: {e}")

    return {
        "data": df_type.to_json(orient="records"),
        "messages": messages
    }
