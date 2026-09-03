from pathlib import Path
import sqlite3
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "database" / "recruitment_dw.db"
SQL_PATH = PROJECT_ROOT / "sql" / "analytical_queries.sql"


def load_sql_queries():
    """
    Read the analytical SQL file and separate each
    analytical query according to its section.
    """

    with open(SQL_PATH, "r", encoding="utf-8") as sql_file:
        sql_content = sql_file.read()

    queries = {}

    sections = [
        (
            "R1 - Hiring Trends",
            "-- R1 - HIRING TRENDS",
            "-- R2 - TECHNOLOGY ANALYSIS"
        ),
        (
            "R2 - Technology Analysis",
            "-- R2 - TECHNOLOGY ANALYSIS",
            "-- R3 - CANDIDATE PROFILE ANALYSIS"
        ),
        (
            "R3 - Candidate Profile Analysis",
            "-- R3 - CANDIDATE PROFILE ANALYSIS",
            "-- R3 - YOE ANALYSIS"
        ),
        (
            "R3 - YOE Analysis",
            "-- R3 - YOE ANALYSIS",
            "-- R4 - TECHNICAL ASSESSMENT EFFECTIVENESS"
        ),
        (
            "R4 - Technical Assessment Effectiveness",
            "-- R4 - TECHNICAL ASSESSMENT EFFECTIVENESS",
            "-- R5 - TECHNOLOGY-ASSESSMENT ANALYSIS"
        ),
        (
            "R5 - Technology-Assessment Analysis",
            "-- R5 - TECHNOLOGY-ASSESSMENT ANALYSIS",
            None
        )
    ]

    for name, start_marker, end_marker in sections:

        start = sql_content.index(start_marker)

        if end_marker:
            end = sql_content.index(end_marker)
            query = sql_content[start:end]
        else:
            query = sql_content[start:]

        queries[name] = query

    return queries

def execute_query(connection, query):
    """
    Execute a SQL query and return the result as a DataFrame.
    """

    return pd.read_sql_query(
        query,
        connection
    )


def main():
    """
    Execute and display all analytical queries.
    """

    print("=" * 70)
    print("ANALYTICAL QUERIES - TEST")
    print("=" * 70)

    print(f"\nDatabase: {DATABASE_PATH}")
    print(f"SQL file: {SQL_PATH}")

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        queries = load_sql_queries()

        for requirement, query in queries.items():

            print("\n" + "=" * 70)
            print(requirement)
            print("=" * 70)

            result = execute_query(
                connection,
                query
            )

            print(result.to_string(index=False))

    finally:
        connection.close()

    print("\n" + "=" * 70)
    print("ANALYTICAL QUERIES TEST COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()