import argparse
import logging
import os
from datetime import datetime

import numpy as np
import pandas as pd

# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("apexplanet_pipeline")



#  Load raw data

def load_data(input_path: str) -> pd.DataFrame:
    logger.info(f"Loading raw data from: {input_path}")
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # Superstore CSV commonly needs latin-1 encoding
    try:
        df = pd.read_csv(input_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(input_path, encoding="latin-1")

    logger.info(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
    return df



#  Clean data

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    logger.info("Cleaning data...")
    df = df.copy()

    # Standardize column names (strip whitespace)
    df.columns = [c.strip() for c in df.columns]

    # Drop exact duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicate rows")

    # Handle missing values: numeric -> median, categorical -> mode
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].median())
            else:
                df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else "Unknown")

    # Fix date columns
    for date_col in ["Order Date", "Ship Date"]:
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors="coerce", dayfirst=False)

    # Fix numeric dtypes
    for num_col in ["Sales", "Profit", "Discount"]:
        if num_col in df.columns:
            df[num_col] = pd.to_numeric(df[num_col], errors="coerce")

    if "Quantity" in df.columns:
        df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0).astype(int)

    # Outlier handling on Sales using IQR (cap instead of drop, to preserve row count)
    if "Sales" in df.columns:
        q1, q3 = df["Sales"].quantile([0.25, 0.75])
        iqr = q3 - q1
        lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        outliers = ((df["Sales"] < lower) | (df["Sales"] > upper)).sum()
        df["Sales"] = df["Sales"].clip(lower=lower, upper=upper)
        logger.info(f"Capped {outliers} Sales outliers using IQR method")

    logger.info(f"Cleaning complete. Final shape: {df.shape}")
    return df


# Calculate KPIs

def calculate_kpis(df: pd.DataFrame) -> dict:
    logger.info("Calculating KPIs...")

    kpis = {
        "Total Orders": int(df["Order ID"].nunique()) if "Order ID" in df.columns else len(df),
        "Total Sales ($)": round(df["Sales"].sum(), 2) if "Sales" in df.columns else None,
        "Total Profit ($)": round(df["Profit"].sum(), 2) if "Profit" in df.columns else None,
        "Average Discount": round(df["Discount"].mean(), 4) if "Discount" in df.columns else None,
        "Average Order Value ($)": round(df["Sales"].mean(), 2) if "Sales" in df.columns else None,
        "Top Category": df.groupby("Category")["Sales"].sum().idxmax() if "Category" in df.columns else None,
        "Top Region (by Profit)": df.groupby("Region")["Profit"].sum().idxmax() if "Region" in df.columns else None,
        "Top State (by Sales)": df.groupby("State")["Sales"].sum().idxmax() if "State" in df.columns else None,
        "Report Generated On": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    for k, v in kpis.items():
        logger.info(f"  {k}: {v}")

    return kpis


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    if "Category" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("Category")
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .round(2)
        .reset_index()
        .sort_values("Total_Sales", ascending=False)
    )


def region_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    if "Region" not in df.columns:
        return pd.DataFrame()
    return (
        df.groupby("Region")
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
        .round(2)
        .reset_index()
        .sort_values("Total_Profit", ascending=False)
    )


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    if "Order Date" not in df.columns:
        return pd.DataFrame()
    trend = df.set_index("Order Date").resample("ME")["Sales"].sum().round(2).reset_index()
    trend.columns = ["Month", "Total_Sales"]
    return trend



# Save processed data + export to Excel

def save_outputs(df: pd.DataFrame, kpis: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    processed_csv = os.path.join(output_dir, "processed_superstore.csv")
    df.to_csv(processed_csv, index=False)
    logger.info(f"Saved cleaned dataset -> {processed_csv}")

    excel_path = os.path.join(output_dir, "ApexPlanet_KPI_Report.xlsx")
    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
        pd.DataFrame(list(kpis.items()), columns=["KPI", "Value"]).to_excel(
            writer, sheet_name="KPI Summary", index=False
        )
        category_breakdown(df).to_excel(writer, sheet_name="By Category", index=False)
        region_breakdown(df).to_excel(writer, sheet_name="By Region", index=False)
        monthly_trend(df).to_excel(writer, sheet_name="Monthly Trend", index=False)
        df.to_excel(writer, sheet_name="Cleaned Data", index=False)

    logger.info(f"Saved KPI Excel report -> {excel_path}")
    return processed_csv, excel_path


# Main pipeline

def run_pipeline(input_path: str, output_dir: str):
    logger.info("=" * 60)
    logger.info("ApexPlanet Automated Data Pipeline - Starting")
    logger.info("=" * 60)

    df_raw = load_data(input_path)
    df_clean = clean_data(df_raw)
    kpis = calculate_kpis(df_clean)
    processed_csv, excel_path = save_outputs(df_clean, kpis, output_dir)

    logger.info("=" * 60)
    logger.info("Pipeline completed successfully!")
    logger.info(f"  Cleaned CSV : {processed_csv}")
    logger.info(f"  KPI Excel   : {excel_path}")
    logger.info("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ApexPlanet Superstore automated pipeline")
    parser.add_argument("--input", default=r"C:\Users\Igrit\OneDrive\Desktop\Task_5\superstore.csv",
                         help="Path to raw Superstore CSV")
    parser.add_argument("--output", default="reports", help="Folder to save cleaned data + Excel report")
    args = parser.parse_args()

    run_pipeline(args.input, args.output)