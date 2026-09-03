from pathlib import Path
import pandas as pd

from sqlalchemy import create_engine, text


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SQL_PATH = PROJECT_ROOT / "sql" / "create_tables.sql"

# ------------------------------------------------------------
# MySQL connection configuration
# ------------------------------------------------------------
# Modify these values according to your MySQL installation.

MYSQL_USER = "root"
MYSQL_PASSWORD = "Clon1789"
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
DATABASE_NAME = "recruitment_dw"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def create_database_engine():
    """
    Create a SQLAlchemy engine connected to the MySQL database.
    """

    connection_url = (
        f"mysql+pymysql://"
        f"{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/"
        f"{DATABASE_NAME}"
    )

    engine = create_engine(connection_url)

    return engine


# ============================================================
# DATABASE CREATION
# ============================================================

def create_database():
    """
    Create the recruitment_dw database if it does not exist.

    The connection is made to the MySQL server without selecting
    a specific database first.
    """

    server_url = (
        f"mysql+pymysql://"
        f"{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}"
    )

    engine = create_engine(server_url)

    with engine.connect() as connection:
        connection.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}"
            )
        )
        connection.commit()

    engine.dispose()

    print("Database verified successfully.")


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables(engine):
    """
    Execute the SQL schema used by the dimensional model.

    The SQL file creates the dimensions and fact table,
    including primary keys, foreign keys, constraints and indexes.
    """

    with open(SQL_PATH, "r", encoding="utf-8") as file:
        sql_script = file.read()

    # --------------------------------------------------------
    # Remove database-level commands from the SQL script.
    #
    # The database itself is already created by create_database().
    # The engine is already connected to recruitment_dw.
    # --------------------------------------------------------

    statements = []

    for statement in sql_script.split(";"):
        statement = statement.strip()

        if not statement:
            continue

        if statement.upper().startswith("CREATE DATABASE"):
            continue

        if statement.upper().startswith("USE "):
            continue

        statements.append(statement)

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))

    print("Database schema recreated successfully.")


# ============================================================
# RESET DATABASE
# ============================================================

def reset_database(engine):
    """
    Recreate the dimensional model from scratch.

    Fact table is dropped first because it references
    the dimension tables through foreign keys.
    """

    print("\nRESETTING DATABASE")

    with engine.begin() as connection:

        connection.execute(
            text("DROP TABLE IF EXISTS Fact_Application")
        )

        connection.execute(
            text("DROP TABLE IF EXISTS Dim_Profile")
        )

        connection.execute(
            text("DROP TABLE IF EXISTS Dim_Technology")
        )

        connection.execute(
            text("DROP TABLE IF EXISTS Dim_Date")
        )

    create_tables(engine)


# ============================================================
# LOAD DIMENSIONS
# ============================================================

def load_dimensions(
    engine,
    dim_date,
    dim_technology,
    dim_profile
):
    """
    Load the three dimension tables into MySQL.

    Existing table structures are preserved using append.
    """

    print("\nLOADING DIMENSIONS")

    # --------------------------------------------------------
    # Dim_Date
    # --------------------------------------------------------

    dim_date = dim_date.rename(
        columns={
            "Application Date": "Application_Date"
        }
    )

    dim_date.to_sql(
        "Dim_Date",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Dim_Date loaded: {len(dim_date)} rows")

    # --------------------------------------------------------
    # Dim_Technology
    # --------------------------------------------------------

    dim_technology.to_sql(
        "Dim_Technology",
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Dim_Technology loaded: "
        f"{len(dim_technology)} rows"
    )

    # --------------------------------------------------------
    # Dim_Profile
    # --------------------------------------------------------

    dim_profile.to_sql(
        "Dim_Profile",
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Dim_Profile loaded: "
        f"{len(dim_profile)} rows"
    )


# ============================================================
# LOAD FACT TABLE
# ============================================================

def load_fact(engine, fact_application):
    """
    Load the Fact_Application table into MySQL.
    """

    print("\nLOADING FACT TABLE")

    fact_application.to_sql(
        "Fact_Application",
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Fact_Application loaded: "
        f"{len(fact_application)} rows"
    )


# ============================================================
# VALIDATE LOAD
# ============================================================

def validate_load(engine):
    """
    Validate the loaded dimensional model.

    Checks:
    - Row counts
    - Primary key uniqueness
    - Foreign key integrity
    - Hiring outcome distribution
    """

    print("\nLOAD VALIDATION")

    # --------------------------------------------------------
    # ROW COUNTS
    # --------------------------------------------------------

    print("\nROW COUNTS")

    tables = [
        "Dim_Date",
        "Dim_Technology",
        "Dim_Profile",
        "Fact_Application"
    ]

    for table in tables:

        query = text(
            f"SELECT COUNT(*) AS row_count "
            f"FROM {table}"
        )

        with engine.connect() as connection:
            result = connection.execute(query).scalar()

        print(f"{table}: {result}")

    # --------------------------------------------------------
    # PRIMARY KEY VALIDATION
    # --------------------------------------------------------

    print("\nPRIMARY KEY VALIDATION")

    primary_keys = {
        "Dim_Date": "Date_Key",
        "Dim_Technology": "Technology_Key",
        "Dim_Profile": "Profile_Key",
        "Fact_Application": "Application_Key"
    }

    for table, primary_key in primary_keys.items():

        query = text(
            f"""
            SELECT
                COUNT(*) AS total_rows,
                COUNT(DISTINCT {primary_key}) AS unique_keys
            FROM {table}
            """
        )

        with engine.connect() as connection:
            result = connection.execute(query).fetchone()

        total_rows = result[0]
        unique_keys = result[1]

        status = "OK" if total_rows == unique_keys else "ERROR"

        print(
            f"{table}.{primary_key}: "
            f"{status} "
            f"(rows={total_rows}, "
            f"unique_keys={unique_keys})"
        )

    # --------------------------------------------------------
    # FOREIGN KEY VALIDATION
    # --------------------------------------------------------

    print("\nFOREIGN KEY VALIDATION")

    foreign_key_checks = {

        "Date_Key": """
            SELECT COUNT(*)
            FROM Fact_Application f
            LEFT JOIN Dim_Date d
                ON f.Date_Key = d.Date_Key
            WHERE d.Date_Key IS NULL
        """,

        "Technology_Key": """
            SELECT COUNT(*)
            FROM Fact_Application f
            LEFT JOIN Dim_Technology t
                ON f.Technology_Key = t.Technology_Key
            WHERE t.Technology_Key IS NULL
        """,

        "Profile_Key": """
            SELECT COUNT(*)
            FROM Fact_Application f
            LEFT JOIN Dim_Profile p
                ON f.Profile_Key = p.Profile_Key
            WHERE p.Profile_Key IS NULL
        """
    }

    total_fk_violations = 0

    with engine.connect() as connection:

        for fk_name, query in foreign_key_checks.items():

            violations = connection.execute(
                text(query)
            ).scalar()

            total_fk_violations += violations

    if total_fk_violations == 0:
        print("Foreign keys: OK (no violations)")
    else:
        print(
            f"Foreign keys: ERROR "
            f"({total_fk_violations} violations)"
        )

    # --------------------------------------------------------
    # HIRING OUTCOME VALIDATION
    # --------------------------------------------------------

    print("\nHIRING OUTCOME VALIDATION")

    query = text(
        """
        SELECT COUNT(*)
        FROM Fact_Application
        WHERE Hiring_Outcome NOT IN (0, 1)
        """
    )

    with engine.connect() as connection:
        invalid_outcomes = connection.execute(query).scalar()

    if invalid_outcomes == 0:
        print("Hiring_Outcome: OK")
    else:
        print(
            f"Hiring_Outcome: ERROR "
            f"({invalid_outcomes} invalid values)"
        )

    # --------------------------------------------------------
    # HIRING DISTRIBUTION
    # --------------------------------------------------------

    print("\nHIRING DISTRIBUTION")

    query = text(
        """
        SELECT
            Hiring_Outcome,
            COUNT(*) AS total
        FROM Fact_Application
        GROUP BY Hiring_Outcome
        ORDER BY Hiring_Outcome
        """
    )

    with engine.connect() as connection:
        results = connection.execute(query).fetchall()

    for outcome, total in results:

        if outcome == 1:
            label = "HIRED"
        else:
            label = "NOT HIRED"

        print(f"{label}: {total}")


# ============================================================
# COMPLETE LOAD PROCESS
# ============================================================

def load_data(
    dim_date,
    dim_technology,
    dim_profile,
    fact_application
):
    """
    Execute the complete database loading process.
    """

    # --------------------------------------------------------
    # 1. Create database
    # --------------------------------------------------------

    create_database()

    # --------------------------------------------------------
    # 2. Connect to database
    # --------------------------------------------------------

    engine = create_database_engine()

    try:

        # ----------------------------------------------------
        # 3. Reset and recreate schema
        # ----------------------------------------------------

        reset_database(engine)

        # ----------------------------------------------------
        # 4. Load dimensions
        # ----------------------------------------------------

        load_dimensions(
            engine,
            dim_date,
            dim_technology,
            dim_profile
        )

        # ----------------------------------------------------
        # 5. Load fact
        # ----------------------------------------------------

        load_fact(
            engine,
            fact_application
        )

        # ----------------------------------------------------
        # 6. Validate
        # ----------------------------------------------------

        validate_load(engine)

    finally:

        engine.dispose()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    from extract import extract_data
    from transform import (
        prepare_data,
        transform_business_rules
    )
    from dimensional_model import build_dimensional_model

    print("STARTING ETL LOAD PROCESS")

    # --------------------------------------------------------
    # EXTRACT
    # --------------------------------------------------------

    df_raw = extract_data()

    # --------------------------------------------------------
    # DATA PREPARATION
    # --------------------------------------------------------

    df_prepared = prepare_data(df_raw)

    # --------------------------------------------------------
    # BUSINESS TRANSFORMATION
    # --------------------------------------------------------

    df_transformed = transform_business_rules(
        df_prepared
    )

    # --------------------------------------------------------
    # DIMENSIONAL TRANSFORMATION
    # --------------------------------------------------------

    (
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    ) = build_dimensional_model(
        df_transformed
    )

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    load_data(
        dim_date,
        dim_technology,
        dim_profile,
        fact_application
    )

    print("\nETL LOAD PROCESS COMPLETED")