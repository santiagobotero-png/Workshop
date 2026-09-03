from extract import extract_data
from transform import prepare_data, transform_business_rules
from dimensional_model import build_dimensional_model
from load import load_data


def main():
    """
    Execute the complete ETL pipeline.

    Pipeline:
    1. Extract source data
    2. Prepare data
    3. Apply business rules
    4. Build dimensional model
    5. Load data into the data warehouse
    """

    print("=" * 60)
    print("RECRUITMENT DATA WAREHOUSE - ETL PIPELINE")
    print("=" * 60)

    # --------------------------------------------------------
    # 1. EXTRACT
    # --------------------------------------------------------

    print("\n[1/5] EXTRACT")
    print("-" * 60)

    df_raw = extract_data()

    print(f"Extracted rows: {len(df_raw)}")
    print(f"Extracted columns: {len(df_raw.columns)}")

    # --------------------------------------------------------
    # 2. DATA PREPARATION
    # --------------------------------------------------------

    print("\n[2/5] DATA PREPARATION")
    print("-" * 60)

    df_prepared = prepare_data(df_raw)

    print(f"Prepared rows: {len(df_prepared)}")
    print(f"Prepared columns: {len(df_prepared.columns)}")

    # --------------------------------------------------------
    # 3. BUSINESS TRANSFORMATION
    # --------------------------------------------------------

    print("\n[3/5] BUSINESS TRANSFORMATION")
    print("-" * 60)

    df_transformed = transform_business_rules(df_prepared)

    print(f"Transformed rows: {len(df_transformed)}")
    print(f"Transformed columns: {len(df_transformed.columns)}")

    # --------------------------------------------------------
    # 4. DIMENSIONAL TRANSFORMATION
    # --------------------------------------------------------

    print("\n[4/5] DIMENSIONAL TRANSFORMATION")
    print("-" * 60)

    (
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    ) = build_dimensional_model(df_transformed)

    print(f"Dim_Date: {len(dim_date)} rows")
    print(f"Dim_Technology: {len(dim_technology)} rows")
    print(f"Dim_Profile: {len(dim_profile)} rows")
    print(f"Fact_Application: {len(fact_application)} rows")

    # --------------------------------------------------------
    # 5. LOAD
    # --------------------------------------------------------

    print("\n[5/5] LOAD")
    print("-" * 60)

    load_data(
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    )

    print("\n" + "=" * 60)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()