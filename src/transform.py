from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "candidates.csv"


def prepare_data(df):
    """
    Prepare the extracted data for the analytical model.

    This function performs only data preparation:
    - Correct data types
    - Standardize relevant categorical values
    - Validate missing values
    - Validate duplicate records

    No business rules or derived business attributes
    are created at this stage.
    """

    df = df.copy()

    # 1. Correct data types
    df["Application Date"] = pd.to_datetime(
        df["Application Date"],
        errors="coerce"
    )

    df["YOE"] = pd.to_numeric(
        df["YOE"],
        errors="coerce"
    )

    df["Code Challenge Score"] = pd.to_numeric(
        df["Code Challenge Score"],
        errors="coerce"
    )

    df["Technical Interview Score"] = pd.to_numeric(
        df["Technical Interview Score"],
        errors="coerce"
    )

    # 2. Standardize relevant categorical attributes
    categorical_columns = [
        "Seniority",
        "Technology"
    ]

    for column in categorical_columns:
        df[column] = df[column].astype("string").str.strip()

    # 3. Validate missing values
    missing_values = df.isnull().sum()

    if missing_values.sum() > 0:
        print("\nWARNING: Missing values detected:")
        print(missing_values[missing_values > 0])
    else:
        print("\nNo missing values detected.")

    # 4. Validate duplicate records
    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:
        print(f"\nWARNING: {duplicate_count} exact duplicate records detected.")
    else:
        print("\nNo exact duplicate records detected.")

    return df


def transform_business_rules(df):
    """
    Apply business rules and create analytically relevant
    derived attributes.
    """

    df = df.copy()

    # Business rule:
    # HIRED if both technical assessments are >= 7
    df["Hiring_Outcome"] = (
        (df["Code Challenge Score"] >= 7) &
        (df["Technical Interview Score"] >= 7)
    ).astype(int)

    # Validation
    hired_count = (df["Hiring_Outcome"] == 1).sum()
    not_hired_count = (df["Hiring_Outcome"] == 0).sum()

    print("\nBUSINESS TRANSFORMATION")
    print(f"HIRED: {hired_count}")
    print(f"NOT HIRED: {not_hired_count}")
    print(f"TOTAL: {len(df)}")

    return df


if __name__ == "__main__":

    # Extract source data
    df_raw = pd.read_csv(
        DATA_PATH,
        sep=";"
    )

    # 10.2 Data Preparation
    df_prepared = prepare_data(df_raw)

    # 10.3 Business Transformation
    df_transformed = transform_business_rules(df_prepared)

    print("\nBUSINESS TRANSFORMATION COMPLETED")
    print(f"Rows: {df_transformed.shape[0]}")
    print(f"Columns: {df_transformed.shape[1]}")

    print("\nHiring outcome distribution:")
    print(df_transformed["Hiring_Outcome"].value_counts())

    print("\nFirst 5 transformed records:")
    print(
        df_transformed[
            [
                "Code Challenge Score",
                "Technical Interview Score",
                "Hiring_Outcome"
            ]
        ].head()
    )