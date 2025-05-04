import numpy as np
import pandas as pd
from sklearn.preprocessing import QuantileTransformer
from scipy.stats import kurtosis, skew
import statsmodels.api as sm

# آوتلایر هندلینگ
def handle_outliers(df, methods: dict):
    df = pd.read_json(df)
    df_outlier = df.copy()
    messages = []

    for col, method in methods.items():
        if col not in df.columns:
            messages.append(f"Column '{col}' not found.")
            continue

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        if method == '1':  # حذف
            df_outlier = df_outlier[(df_outlier[col] >= lower) & (df_outlier[col] <= upper)]
            messages.append(f"Removed outliers in '{col}'.")
        elif method == '2':  # لگ
            df_outlier[col] = np.log(df_outlier[col].replace(0, np.nan))
            messages.append(f"Applied log transformation to '{col}'.")
        elif method == '3':  # Quantile
            qt = QuantileTransformer(output_distribution='normal')
            df_outlier[col] = qt.fit_transform(df_outlier[[col]])
            messages.append(f"Applied quantile transformation to '{col}'.")
        elif method == '4':  # sqrt
            df_outlier[col] = np.sqrt(df_outlier[col].replace(0, np.nan))
            messages.append(f"Applied square root transformation to '{col}'.")
        elif method == '5':  # Box-Cox
            df_outlier[col], _ = sm.stats.boxcox(df_outlier[col].replace(0, np.nan) + 1)
            messages.append(f"Applied Box-Cox transformation to '{col}'.")
        elif method == '6':  # جایگزینی
            val = df_outlier[col].median()
            df_outlier[col] = np.where((df_outlier[col] < lower) | (df_outlier[col] > upper), val, df_outlier[col])
            messages.append(f"Replaced outliers in '{col}' with median.")
        elif method == '7':  # Winsorizing
            df_outlier[col] = np.clip(df_outlier[col], lower, upper)
            messages.append(f"Applied winsorizing to '{col}'.")
        elif method == '8':  # MAD
            med = np.median(df_outlier[col])
            mad = sm.robust.mad(df_outlier[col])
            df_outlier[col] = np.where(df_outlier[col] > 3 * mad + med, 3 * mad + med, df_outlier[col])
            messages.append(f"Applied MAD transformation to '{col}'.")
        elif method == '9':  # Trimming
            df_outlier = df_outlier[(df_outlier[col] >= lower) & (df_outlier[col] <= upper)]
            messages.append(f"Trimmed dataset based on '{col}'.")

    return {
        "data": df_outlier.to_json(orient="records"),
        "messages": messages
    }

# binning ستون‌ها
def bin_columns(df, bin_info: dict):
    df = pd.read_json(df)
    df_bin = df.copy()
    messages = []

    for col, bins in bin_info.items():
        if col not in df.columns:
            messages.append(f"Column '{col}' not found.")
            continue
        try:
            df_bin[col + "_binned"] = pd.cut(df_bin[col], bins=bins, labels=[f"bin_{i+1}" for i in range(bins)])
            messages.append(f"Binned column '{col}' into {bins} bins.")
        except Exception as e:
            messages.append(f"Error binning '{col}': {e}")

    return {
        "data": df_bin.to_json(orient="records"),
        "messages": messages
    }

# وان-هات انکودینگ
def one_hot_encoding(df, columns: list):
    df = pd.read_json(df)
    df_one_hot = df.copy()
    messages = []
    try:
        df_one_hot = pd.get_dummies(df_one_hot, columns=columns)
        messages.append(f"One-hot encoded columns: {', '.join(columns)}.")
    except Exception as e:
        messages.append(f"Error during one-hot encoding: {e}")

    return {
        "data": df_one_hot.to_json(orient="records"),
        "messages": messages
    }

# همبستگی‌ها
def handle_correlation(df, threshold_pearson=0.7, threshold_spearman=0.7):
    df = pd.read_json(df)
    messages = []

    try:
        pearson_corr = df.corr(method='pearson')
        spearman_corr = df.corr(method='spearman')

        strong_pearson = []
        strong_spearman = []

        for col in pearson_corr.columns:
            for idx in pearson_corr.index:
                val = pearson_corr.at[idx, col]
                if col != idx and abs(val) >= threshold_pearson:
                    strong_pearson.append((col, idx, round(val, 2)))

        for col in spearman_corr.columns:
            for idx in spearman_corr.index:
                val = spearman_corr.at[idx, col]
                if col != idx and abs(val) >= threshold_spearman:
                    strong_spearman.append((col, idx, round(val, 2)))

        messages.append(f"Strong Pearson Correlations: {strong_pearson}")
        messages.append(f"Strong Spearman Correlations: {strong_spearman}")
    except Exception as e:
        messages.append(f"Correlation analysis failed: {e}")

    return {
        "data": df.to_json(orient="records"),
        "messages": messages
    }
