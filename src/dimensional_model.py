from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def build_date_dimension(df):
    """
    Create the Date dimension from distinct application dates.

    Each row represents one distinct application date.
    A surrogate key is generated for each date.
    """

    dim_date = (
        df[["Application Date"]]
        .drop_duplicates()
        .sort_values("Application Date")
        .reset_index(drop=True)
    )

    # Generate surrogate key
    dim_date.insert(
        0,
        "Date_Key",
        range(1, len(dim_date) + 1)
    )

    # Derived calendar attributes
    dim_date["Day"] = dim_date["Application Date"].dt.day
    dim_date["Month"] = dim_date["Application Date"].dt.month
    dim_date["Quarter"] = dim_date["Application Date"].dt.quarter
    dim_date["Year"] = dim_date["Application Date"].dt.year

    return dim_date


def build_technology_dimension(df):
    """
    Create the Technology dimension.

    Duplicate technology values are removed and
    a surrogate key is generated for each technology.
    """

    dim_technology = (
        df[["Technology"]]
        .drop_duplicates()
        .sort_values("Technology")
        .reset_index(drop=True)
    )

    # Generate surrogate key
    dim_technology.insert(
        0,
        "Technology_Key",
        range(1, len(dim_technology) + 1)
    )

    return dim_technology


def build_profile_dimension(df):
    """
    Create the Profile dimension from distinct seniority levels.

    Duplicate seniority values are removed and
    a surrogate key is generated for each profile.
    """

    dim_profile = (
        df[["Seniority"]]
        .drop_duplicates()
        .sort_values("Seniority")
        .reset_index(drop=True)
    )

    # Generate surrogate key
    dim_profile.insert(
        0,
        "Profile_Key",
        range(1, len(dim_profile) + 1)
    )

    return dim_profile


def build_fact_application(
    df,
    dim_date,
    dim_technology,
    dim_profile
):
    """
    Create Fact_Application according to the declared grain:

    One row represents one individual application submitted
    by a candidate to the recruitment process.
    """

    fact = df.copy()

    # Map Application Date → Date_Key
    fact = fact.merge(
        dim_date[["Date_Key", "Application Date"]],
        on="Application Date",
        how="left",
        validate="many_to_one"
    )

    # Map Technology → Technology_Key
    fact = fact.merge(
        dim_technology[["Technology_Key", "Technology"]],
        on="Technology",
        how="left",
        validate="many_to_one"
    )

    # Map Seniority → Profile_Key
    fact = fact.merge(
        dim_profile[["Profile_Key", "Seniority"]],
        on="Seniority",
        how="left",
        validate="many_to_one"
    )

    # Generate application surrogate key
    fact.insert(
        0,
        "Application_Key",
        range(1, len(fact) + 1)
    )

    # Keep only attributes justified by the analytical requirements
    fact = fact[
        [
            "Application_Key",
            "Date_Key",
            "Technology_Key",
            "Profile_Key",
            "YOE",
            "Code Challenge Score",
            "Technical Interview Score",
            "Hiring_Outcome"
        ]
    ]

    # Rename columns according to the dimensional model
    fact = fact.rename(
        columns={
            "Code Challenge Score": "Code_Challenge_Score",
            "Technical Interview Score": "Technical_Interview_Score"
        }
    )

    return fact


def build_dimensional_model(df):
    """
    Build the complete dimensional model.
    """

    dim_date = build_date_dimension(df)
    dim_technology = build_technology_dimension(df)
    dim_profile = build_profile_dimension(df)

    fact_application = build_fact_application(
        df,
        dim_date,
        dim_technology,
        dim_profile
    )

    return (
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    )


if __name__ == "__main__":

    # Load the transformed data.
    # For now, this reproduces the previous ETL stages
    # so the dimensional model can be tested independently.
    from extract import extract_data
    from transform import prepare_data, transform_business_rules

    # 10.1 Extract
    df_raw = extract_data()

    # 10.2 Data Preparation
    df_prepared = prepare_data(df_raw)

    # 10.3 Business Transformation
    df_transformed = transform_business_rules(df_prepared)

    # Task 4: Dimensional Transformation
    (
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    ) = build_dimensional_model(df_transformed)

    print("\nDIMENSIONAL TRANSFORMATION COMPLETED")

    print("\nDimension sizes:")
    print(f"Dim_Date: {len(dim_date)}")
    print(f"Dim_Technology: {len(dim_technology)}")
    print(f"Dim_Profile: {len(dim_profile)}")
    print(f"Fact_Application: {len(fact_application)}")

    print("\nDim_Date:")
    print(dim_date.head())

    print("\nDim_Technology:")
    print(dim_technology)

    print("\nDim_Profile:")
    print(dim_profile)

    print("\nFact_Application:")
    print(fact_application.head())