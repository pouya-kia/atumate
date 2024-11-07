import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import QuantileTransformer
from scipy.stats import kurtosis, skew, spearmanr, pearsonr
import statsmodels.api as sm
import scipy.stats as stats
import pandas as pd

# Function to visualize boxplot and histogram for each column
def visualize_columns(df):
    # Ask the user if they want to visualize the data
    visualize_choice = input(
        "Do you want to visualize the columns with boxplot and histogram? (yes/no): ").strip().lower()

    if visualize_choice == 'no':
        print("Skipping visualizations.")
        return

    # Iterate over each column in the dataframe
    for column in df.columns:
        if df[column].dtype in ['int64', 'float64']:  # Visualize only numeric columns
            plt.figure(figsize=(12, 6))

            # Boxplot
            plt.subplot(1, 2, 1)
            sns.boxplot(x=df[column])
            plt.title(f'Boxplot of {column}')

            # Histogram
            plt.subplot(1, 2, 2)
            sns.histplot(df[column], kde=True, bins=20)
            plt.title(f'Histogram of {column}')

            plt.tight_layout()
            plt.show()


# Function to calculate IQR and identify outliers
def calculate_iqr_outliers(df):
    print("\nOutlier Detection using IQR:")
    print("Formula: Lower Bound = Q1 - 1.5 * IQR, Upper Bound = Q3 + 1.5 * IQR\n")

    outliers_info = {}
    for column in df.select_dtypes(include=[np.number]).columns:
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        num_outliers = len(outliers)
        skew_ = skew(df[column])
        kurtosis_ = kurtosis(df[column])
        outliers_info[column] = {'lower_bound': lower_bound, 'upper_bound': upper_bound, 'num_outliers': num_outliers
            , 'skew': skew_, 'kurtosis': kurtosis_}

        print(f"Column: {column}")
        print(f"Lower Bound: {lower_bound}, Upper Bound: {upper_bound}")
        print(f"Number of outliers: {num_outliers}")
        print(f"skew : {skew_}")
        print(f"kurtosis : {kurtosis_}\n")

    return outliers_info


# Function to ask user if they want to handle outliers
def handle_outliers(df):
    df_outlier = df.copy()
    handle_choice = input("Do you want to handle outliers? (yes/no): ").strip().lower()
    if handle_choice == 'no':
        print("Skipping outlier handling.")
        return df_outlier

    # Show outlier detection based on IQR
    outliers_info = calculate_iqr_outliers(df_outlier)

    # Ask if user wants to continue handling outliers
    handle_choice = input("Do you want to handle outliers after that seeing the results? (yes/no): ").strip().lower()
    if handle_choice == 'no':
        return df_outlier

    print("\nAvailable Methods for Handling Outliers:")
    print("Removal Methods:")
    print("1. Delete Outliers (Remove rows outside IQR bounds)")
    print("Transformation Methods:")
    print("2. Log Transformation")
    print("3. QuantileTransformer")
    print("4. Square Root Transformation")
    print("5. Box-Cox Transformation")
    print("Replacement Methods:")
    print("6. Replace with Median/Mean")
    print("7. Winsorizing (Capping/Flooring)")
    print("Robust Statistical Methods:")
    print("8. Median & MAD (Median Absolute Deviation)")
    print("Resampling Techniques:")
    print("9. Trimming the Dataset\n")

    # Create a copy of the original dataframe for comparison
    df_original = df_outlier.copy()

    # Ask user which columns and methods to apply
    methods = {}
    while True:
        user_input = input(
            "Enter the columns and methods in the format (column, method_number). (column2, method_number), ... or type 'done' to finish: ")
        if user_input.lower() == 'done':
            break

        # Split the user input into individual column-method pairs
        pairs = user_input.split('.')
        valid_input = True  # Flag to track validity of user input
        for pair in pairs:
            try:
                pair = pair.strip().strip('()')
                col, method_number = pair.split(',')
                col = col.strip()
                method_number = method_number.strip()
                if col in outliers_info and method_number in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    methods[col] = method_number
                    print('correct')
                else:
                    print(f"Invalid input for column '{col}' or method '{method_number}'")
                    valid_input = False  # Mark input as invalid
            except ValueError:
                print(f"Invalid input: {pair}. Please use the format (column, method_number).")
                valid_input = False  # Mark input as invalid

        # If invalid input was detected, prompt the user to enter again
        if not valid_input:
            print("Please re-enter valid columns and methods.")
            methods.clear()  # Clear the previous invalid entries
            continue

    # Apply selected methods to the columns
    df_outlier = apply_outlier_methods(df_outlier, methods, outliers_info)

    # Plot the boxplot for columns before and after handling
    for column in methods.keys():
        plot_before_after_boxplot(df_original, df_outlier, column)

    return df_outlier


# Function to apply outlier handling methods
def apply_outlier_methods(df, methods, outliers_info):
    for column, method in methods.items():
        lower_bound = outliers_info[column]['lower_bound']
        upper_bound = outliers_info[column]['upper_bound']

        if method == '1':
            # Remove rows outside the IQR bounds
            df = df[(df[column] > lower_bound) & (df[column] < upper_bound)]
            print(f"Removed outliers from column '{column}'.")

        elif method == '2':
            # Log Transformation
            df[column] = np.log(df[column].replace(0, np.nan))  # Avoid log(0)
            print(f"Applied log transformation to column '{column}'.")

        elif method == '3':
            # Quantile Transformer
            qt = QuantileTransformer(output_distribution='normal')
            df[column] = qt.fit_transform(df[[column]])
            print(f"Applied Quantile Transformation to column '{column}'.")

        elif method == '4':
            # Square Root Transformation
            df[column] = np.sqrt(df[column].replace(0, np.nan))  # Avoid sqrt(0)
            print(f"Applied square root transformation to column '{column}'.")

        elif method == '5':
            # Box-Cox Transformation
            df[column], _ = stats.boxcox(df[column].replace(0, np.nan) + 1)  # Box-Cox needs positive values
            print(f"Applied Box-Cox transformation to column '{column}'.")

        elif method == '6':
            # Replace with Median/Mean
            replacement_value = df[column].mean() if input(
                f"Replace outliers in '{column}' with mean or median? (mean/median): ").strip().lower() == 'mean' else \
            df[column].median()
            df[column] = np.where((df[column] < lower_bound) | (df[column] > upper_bound), replacement_value,
                                  df[column])
            print(f"Replaced outliers in column '{column}' with {replacement_value}.")

        elif method == '7':
            # Winsorizing (Capping/Flooring)
            df[column] = np.where(df[column] < lower_bound, lower_bound,
                                  np.where(df[column] > upper_bound, upper_bound, df[column]))
            print(f"Applied winsorizing to column '{column}'.")

        elif method == '8':
            # Median & MAD (Median Absolute Deviation)
            med = np.median(df[column])
            ma = sm.robust.mad(df[column])
            df[column] = np.where(df[column] > 3 * ma + med, 3 * ma + med, df[column])
            print(f"Applied Median & MAD to column '{column}'.")

        elif method == '9':
            # Trimming the Dataset
            df = df[(df[column] > lower_bound) & (df[column] < upper_bound)]
            print(f"Trimmed the dataset based on outliers in column '{column}'.")

    return df


# Function to plot boxplot before and after handling outliers for comparison
def plot_before_after_boxplot(df_original, df_modified, column):
    plt.figure(figsize=(12, 6))

    # Create two subplots for before and after
    plt.subplot(1, 2, 1)
    sns.boxplot(df_original[column])
    plt.title(f'Before Outlier Handling: {column}')

    plt.subplot(1, 2, 2)
    sns.boxplot(df_modified[column])
    plt.title(f'After Outlier Handling: {column}')

    plt.tight_layout()
    plt.show()


# Function to find strong correlations based on threshold
def find_strong_correlations(corr_matrix, threshold):
    strong_corr = []
    # Iterate through the correlation matrix and find correlations above the threshold
    for col in corr_matrix.columns:
        for idx, val in corr_matrix[col].items():
            if abs(val) >= threshold and col != idx:
                strong_corr.append({'Variable 1': col, 'Variable 2': idx, 'Correlation': val})

    # Convert the list to a dataframe for easy display
    return pd.DataFrame(strong_corr).drop_duplicates(subset=['Variable 1', 'Variable 2']).sort_values(by='Correlation',
                                                                                                      ascending=False)


# Function to calculate correlation and visualize
def handle_correlation(df):
    # Ask user if they want to calculate and visualize correlation
    correlation_choice = input("Do you want to calculate and visualize correlations? (yes/no): ").strip().lower()
    if correlation_choice == 'no':
        print("Skipping correlation calculation and visualization.")
        return

    # Calculate the Pearson correlation matrix
    pearson_corr = df.corr(method='pearson')
    print("\nPearson Correlation Matrix:")
    print(pearson_corr)

    # Visualize the correlation matrix
    plt.figure(figsize=(12, 8))
    sns.heatmap(pearson_corr, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title("Correlation Matrix (Pearson)")
    plt.show()

    # Ask user if they want to see high correlations
    high_corr_choice = input("Do you want to see strong linear correlations? (yes/no): ").strip().lower()
    if high_corr_choice == 'yes':
        threshold = float(input("Specify the threshold for strong linear correlation (e.g., 0.7): "))
        strong_linear_corr = find_strong_correlations(pearson_corr, threshold)
        print("\nStrong Linear Correlations:")
        print(strong_linear_corr)

    # Calculate the Spearman correlation matrix
    spearman_corr = df.corr(method='spearman')

    # Ask user if they want to see non-linear correlations
    nonlinear_corr_choice = input("Do you want to see non-linear correlations (Spearman)? (yes/no): ").strip().lower()
    if nonlinear_corr_choice == 'yes':
        spearman_threshold = float(input("Specify the threshold for strong non-linear correlation (e.g., 0.7): "))
        strong_nonlinear_corr = find_strong_correlations(spearman_corr, spearman_threshold)
        print("\nDetected Nonlinear Correlations (Spearman > {0} or < -{0}):".format(spearman_threshold))
        print(strong_nonlinear_corr)

    # Show all results together
    print("\nResults Summary:")
    print("\nStrong Linear Correlations:")
    print(strong_linear_corr)
    print("\nDetected Nonlinear Correlations (Spearman):")
    print(strong_nonlinear_corr)


# Function to ask user if they want to drop columns
# def drop_columns(df):
#     drop_col_choice = input("Do you want to drop any columns? (yes/no): ").strip().lower()
#
#     if drop_col_choice == 'no':
#         print("No columns will be dropped.")
#         return df
#
#     # Ask user for the columns to drop
#     cols_to_drop = input("Enter the columns you want to drop, separated by commas (e.g., col1, col2): ").strip()
#
#     # Split the input into a list and drop the specified columns
#     cols_to_drop = [col.strip() for col in cols_to_drop.split(',')]
#
#     # Drop the columns
#     df.drop(columns=cols_to_drop, inplace=True)
#
#     print(f"Dropped columns: {', '.join(cols_to_drop)}")
#
#     return df


# Function to ask user if they want to bin columns
def bin_columns(df):
    df_bin = df.copy()
    binning_choice = input("Do you want to bin any columns? (yes/no): ").strip().lower()

    if binning_choice == 'no':
        print("No binning will be performed.")
        return df_bin

    # Ask user for the columns to bin
    cols_to_bin = input("Enter the columns you want to bin, separated by commas (col1, col2, e.g.): ").strip()
    cols_to_bin = [col.strip() for col in cols_to_bin.split(',')]

    # For each column, ask the user for the number of bins and bin the column
    for col in cols_to_bin:
        num_bins = int(input(f"Enter the number of bins for column {col}: ").strip())
        df_bin[col + '_binned'] = pd.cut(df_bin[col], bins=num_bins, labels=[f"bin_{i + 1}" for i in range(num_bins)])
        print(f"Column {col} binned into {num_bins} bins.")

    return df_bin


# Function to ask user if they want to do one-hot encoding
def one_hot_encoding(df):
    df_one_hot = df.copy()
    one_hot_choice = input("Do you want to perform one-hot encoding on any columns? (yes/no): ").strip().lower()

    if one_hot_choice == 'no':
        print("No one-hot encoding will be performed.")
        return df_one_hot

    # Ask user for the columns to one-hot encode
    cols_to_encode = input(
        "Enter the columns you want to one-hot encode, separated by commas (e.g., col1, col2): ").strip()
    cols_to_encode = [col.strip() for col in cols_to_encode.split(',')]

    # Perform one-hot encoding on the specified columns
    df_one_hot = pd.get_dummies(df_one_hot, columns=cols_to_encode)

    print(f"One-hot encoding performed on: {', '.join(cols_to_encode)}")

    return df_one_hot