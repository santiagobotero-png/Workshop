# ============================================================
# DATA PROFILING
# Technology Recruitment Analytical System
# ============================================================

import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# 1. CONFIGURATION
# ============================================================

# Project root:
# workshop-1/
# ├── data/
# │   └── raw/
# │       └── candidates.csv
# └── notebooks/
#     └── data_profiling.py

DATA_PATH = Path("data/raw/candidates.csv")


# ============================================================
# 2. LOAD DATA
# ============================================================

print("=" * 70)
print("DATA PROFILING - TECHNOLOGY RECRUITMENT")
print("=" * 70)

print("\n[1] Loading dataset...")

df = pd.read_csv(
    DATA_PATH,
    sep=";"
)

print("Dataset loaded successfully.")


# ============================================================
# 3. BASIC DATASET INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("[2] BASIC DATASET INFORMATION")
print("=" * 70)

rows, columns = df.shape

print(f"Number of rows: {rows}")
print(f"Number of columns: {columns}")


# ============================================================
# 4. COLUMN NAMES
# ============================================================

print("\n" + "=" * 70)
print("[3] COLUMN NAMES")
print("=" * 70)

for index, column in enumerate(df.columns, start=1):
    print(f"{index}. {column}")


# ============================================================
# 5. FIRST RECORDS
# ============================================================

print("\n" + "=" * 70)
print("[4] FIRST 5 RECORDS")
print("=" * 70)

print(df.head().to_string(index=False))


# ============================================================
# 6. DATA TYPES
# ============================================================

print("\n" + "=" * 70)
print("[5] DATA TYPES")
print("=" * 70)

print(df.dtypes)


# ============================================================
# 7. CONVERT APPLICATION DATE
# ============================================================

print("\n" + "=" * 70)
print("[6] APPLICATION DATE CONVERSION")
print("=" * 70)

df["Application Date"] = pd.to_datetime(
    df["Application Date"],
    errors="coerce"
)

print("Application Date converted to datetime.")

print("\nUpdated data types:")
print(df.dtypes)


# ============================================================
# 8. MISSING VALUES
# ============================================================

print("\n" + "=" * 70)
print("[7] MISSING VALUES")
print("=" * 70)

missing_count = df.isnull().sum()

missing_percentage = (
    df.isnull().sum() / len(df) * 100
).round(2)

missing_summary = pd.DataFrame({
    "Missing Count": missing_count,
    "Missing Percentage": missing_percentage
})

print(missing_summary.to_string())

total_missing = df.isnull().sum().sum()

print(f"\nTotal missing values: {total_missing}")


# ============================================================
# 9. RECORDS WITH MISSING VALUES
# ============================================================

if total_missing > 0:

    print("\nRecords containing missing values:")

    missing_records = df[
        df.isnull().any(axis=1)
    ]

    print(
        missing_records.to_string(index=False)
    )

else:

    print("\nNo records contain missing values.")


# ============================================================
# 10. EXACT DUPLICATE RECORDS
# ============================================================

print("\n" + "=" * 70)
print("[8] EXACT DUPLICATE RECORDS")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(f"Exact duplicate records: {duplicate_count}")

if duplicate_count > 0:

    duplicates = df[
        df.duplicated(keep=False)
    ].sort_values(
        by=["Email", "Application Date"]
    )

    print("\nDuplicated records:")
    print(
        duplicates.to_string(index=False)
    )

else:

    print("No exact duplicate records found.")


# ============================================================
# 11. UNIQUE VALUES IN CATEGORICAL ATTRIBUTES
# ============================================================

print("\n" + "=" * 70)
print("[9] CATEGORICAL ATTRIBUTES")
print("=" * 70)

categorical_columns = [
    "Country",
    "Seniority",
    "Technology"
]

for column in categorical_columns:

    print("\n" + "-" * 70)
    print(f"{column}")
    print("-" * 70)

    unique_count = df[column].nunique(
        dropna=True
    )

    print(f"Number of unique values: {unique_count}")

    print("\nValues and frequencies:")

    frequencies = (
        df[column]
        .value_counts(dropna=False)
    )

    print(frequencies.to_string())


# ============================================================
# 12. APPLICATION DATE RANGE
# ============================================================

print("\n" + "=" * 70)
print("[10] APPLICATION DATE RANGE")
print("=" * 70)

min_date = df["Application Date"].min()
max_date = df["Application Date"].max()

print(f"Minimum application date: {min_date}")
print(f"Maximum application date: {max_date}")

if pd.notna(min_date) and pd.notna(max_date):

    period = max_date - min_date

    print(f"Total application period: {period}")


# ============================================================
# 13. APPLICATIONS BY YEAR
# ============================================================

print("\n" + "=" * 70)
print("[11] APPLICATIONS BY YEAR")
print("=" * 70)

df["Application Year"] = (
    df["Application Date"].dt.year
)

applications_by_year = (
    df["Application Year"]
    .value_counts()
    .sort_index()
)

print(
    applications_by_year.to_string()
)


# ============================================================
# 14. SCORE RANGES
# ============================================================

print("\n" + "=" * 70)
print("[12] SCORE RANGES")
print("=" * 70)

score_columns = [
    "Code Challenge Score",
    "Technical Interview Score"
]

score_range = pd.DataFrame({
    "Minimum": df[score_columns].min(),
    "Maximum": df[score_columns].max()
})

print(
    score_range.to_string()
)


# ============================================================
# 15. SCORE VALIDATION
# Expected range: 0 - 10
# ============================================================

print("\n" + "=" * 70)
print("[13] SCORE VALIDATION")
print("=" * 70)

for column in score_columns:

    invalid_scores = df[
        (df[column] < 0) |
        (df[column] > 10)
    ]

    print(
        f"{column}: "
        f"{len(invalid_scores)} values outside "
        f"the expected range [0, 10]"
    )

    if len(invalid_scores) > 0:

        print("\nInvalid records:")

        print(
            invalid_scores[
                [
                    "Email",
                    column
                ]
            ].to_string(index=False)
        )


# ============================================================
# 16. NUMERICAL DESCRIPTIVE STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("[14] DESCRIPTIVE STATISTICS")
print("=" * 70)

numeric_columns = [
    "YOE",
    "Code Challenge Score",
    "Technical Interview Score"
]

descriptive_statistics = (
    df[numeric_columns]
    .describe()
    .round(2)
)

print(
    descriptive_statistics.to_string()
)


# ============================================================
# 17. ADDITIONAL NUMERICAL STATISTICS
# ============================================================

print("\n" + "=" * 70)
print("[15] ADDITIONAL NUMERICAL STATISTICS")
print("=" * 70)

additional_statistics = (
    df[numeric_columns]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
    .round(2)
)

print(
    additional_statistics.to_string()
)


# ============================================================
# 18. YOE VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("[16] YEARS OF EXPERIENCE VALIDATION")
print("=" * 70)

print(
    f"Minimum YOE: {df['YOE'].min()}"
)

print(
    f"Maximum YOE: {df['YOE'].max()}"
)

negative_yoe = df[
    df["YOE"] < 0
]

print(
    f"Records with negative YOE: "
    f"{len(negative_yoe)}"
)

if len(negative_yoe) > 0:

    print("\nRecords with invalid YOE:")

    print(
        negative_yoe.to_string(index=False)
    )


# ============================================================
# 19. BUSINESS RULE - HIRING OUTCOME
# ============================================================

print("\n" + "=" * 70)
print("[17] HIRING OUTCOME")
print("=" * 70)

print(
    "Business rule:"
)

print(
    "HIRED = Code Challenge Score >= 7 "
    "AND Technical Interview Score >= 7"
)

print(
    "Otherwise = NOT HIRED"
)


df["Hiring Outcome"] = np.where(
    (df["Code Challenge Score"] >= 7) &
    (df["Technical Interview Score"] >= 7),
    "HIRED",
    "NOT HIRED"
)


# ============================================================
# 20. HIRING OUTCOME SUMMARY
# ============================================================

hiring_counts = (
    df["Hiring Outcome"]
    .value_counts()
)

hiring_percentages = (
    df["Hiring Outcome"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

hiring_summary = pd.DataFrame({
    "Candidate Count": hiring_counts,
    "Percentage": hiring_percentages
})

print(
    hiring_summary.to_string()
)


# ============================================================
# 21. TECHNICAL ASSESSMENT PASS/FAIL
# ============================================================

print("\n" + "=" * 70)
print("[18] TECHNICAL ASSESSMENT RESULTS")
print("=" * 70)

df["Code Challenge Passed"] = (
    df["Code Challenge Score"] >= 7
)

df["Technical Interview Passed"] = (
    df["Technical Interview Score"] >= 7
)


print("\nCode Challenge:")
print(
    df["Code Challenge Passed"]
    .value_counts()
    .rename({
        True: "Passed",
        False: "Failed"
    })
    .to_string()
)


print("\nTechnical Interview:")
print(
    df["Technical Interview Passed"]
    .value_counts()
    .rename({
        True: "Passed",
        False: "Failed"
    })
    .to_string()
)


# ============================================================
# 22. VERIFY HIRING BUSINESS RULE
# ============================================================

print("\n" + "=" * 70)
print("[19] BUSINESS RULE VALIDATION")
print("=" * 70)

expected_hiring_outcome = np.where(
    (df["Code Challenge Score"] >= 7) &
    (df["Technical Interview Score"] >= 7),
    "HIRED",
    "NOT HIRED"
)

rule_validation = (
    df["Hiring Outcome"] ==
    expected_hiring_outcome
)

valid_records = rule_validation.sum()
invalid_records = (~rule_validation).sum()

print(
    f"Records satisfying the business rule: "
    f"{valid_records} / {len(df)}"
)

print(
    f"Records violating the business rule: "
    f"{invalid_records}"
)


# ============================================================
# 23. CANDIDATE FREQUENCY BY EMAIL
# ============================================================

print("\n" + "=" * 70)
print("[20] CANDIDATE FREQUENCY")
print("=" * 70)

candidate_frequency = (
    df.groupby("Email")
      .size()
      .reset_index(
          name="Application Count"
      )
      .sort_values(
          "Application Count",
          ascending=False
      )
)

unique_candidates = len(candidate_frequency)

print(
    f"Unique candidates based on Email: "
    f"{unique_candidates}"
)

print("\nTop 20 candidates by number of applications:")

print(
    candidate_frequency
    .head(20)
    .to_string(index=False)
)


# ============================================================
# 24. CANDIDATES WITH MULTIPLE APPLICATIONS
# ============================================================

print("\n" + "=" * 70)
print("[21] REAPPLICATION ANALYSIS")
print("=" * 70)

repeated_candidates = candidate_frequency[
    candidate_frequency["Application Count"] > 1
]

reapplied_count = len(repeated_candidates)

print(
    f"Candidates with multiple applications: "
    f"{reapplied_count}"
)

if unique_candidates > 0:

    reapplication_rate = (
        reapplied_count /
        unique_candidates *
        100
    )

else:

    reapplication_rate = 0


print(
    f"Reapplication rate: "
    f"{reapplication_rate:.2f}%"
)


if reapplied_count > 0:

    print("\nCandidates with multiple applications:")

    print(
        repeated_candidates.to_string(
            index=False
        )
    )

else:

    print(
        "No candidates with multiple applications found."
    )


# ============================================================
# 25. REPEATED APPLICATION DETAILS
# ============================================================

print("\n" + "=" * 70)
print("[22] REPEATED APPLICATION DETAILS")
print("=" * 70)

repeated_emails = repeated_candidates[
    "Email"
]

repeated_applications = (
    df[
        df["Email"].isin(
            repeated_emails
        )
    ]
    .sort_values(
        ["Email", "Application Date"]
    )
)


if len(repeated_applications) > 0:

    columns_to_show = [
        "Email",
        "Application Date",
        "Country",
        "YOE",
        "Seniority",
        "Technology",
        "Code Challenge Score",
        "Technical Interview Score",
        "Hiring Outcome"
    ]

    print(
        repeated_applications[
            columns_to_show
        ].to_string(index=False)
    )

else:

    print(
        "No repeated applications found."
    )


# ============================================================
# 26. APPLICATION HISTORY
# ============================================================

print("\n" + "=" * 70)
print("[23] APPLICATION HISTORY")
print("=" * 70)

applications_sorted = (
    df.sort_values(
        ["Email", "Application Date"]
    )
    .copy()
)


applications_sorted[
    "Previous Application Date"
] = (
    applications_sorted
    .groupby("Email")["Application Date"]
    .shift(1)
)


applications_sorted[
    "Days Since Previous Application"
] = (
    applications_sorted["Application Date"]
    -
    applications_sorted["Previous Application Date"]
).dt.days


reapplications = applications_sorted[
    applications_sorted[
        "Previous Application Date"
    ].notna()
]


if len(reapplications) > 0:

    history_columns = [
        "Email",
        "Previous Application Date",
        "Application Date",
        "Days Since Previous Application",
        "Hiring Outcome"
    ]

    print(
        reapplications[
            history_columns
        ].to_string(index=False)
    )

else:

    print(
        "No subsequent applications found."
    )


# ============================================================
# 27. CANDIDATE OUTCOME HISTORY
# ============================================================

print("\n" + "=" * 70)
print("[24] CANDIDATE HIRING OUTCOME HISTORY")
print("=" * 70)

if len(reapplications) > 0:

    candidate_outcome_history = (
        applications_sorted
        .groupby("Email")["Hiring Outcome"]
        .agg(list)
        .reset_index()
    )

    candidate_outcome_history[
        "Application Count"
    ] = (
        candidate_outcome_history[
            "Hiring Outcome"
        ].apply(len)
    )

    candidate_outcome_history = (
        candidate_outcome_history[
            candidate_outcome_history[
                "Application Count"
            ] > 1
        ]
        .sort_values(
            "Application Count",
            ascending=False
        )
    )

    print(
        candidate_outcome_history
        .to_string(index=False)
    )

else:

    print(
        "No repeated candidates found."
    )


# ============================================================
# 28. FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL DATA PROFILING SUMMARY")
print("=" * 70)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print(
    f"Exact duplicate records: "
    f"{duplicate_count}"
)

print(
    f"Unique candidates by email: "
    f"{unique_candidates}"
)

print(
    f"Candidates with multiple applications: "
    f"{reapplied_count}"
)

print(
    f"Reapplication rate: "
    f"{reapplication_rate:.2f}%"
)

print(
    f"Total missing values: "
    f"{total_missing}"
)

print(
    f"Minimum application date: "
    f"{min_date}"
)

print(
    f"Maximum application date: "
    f"{max_date}"
)

print(
    f"Code Challenge Score range: "
    f"{df['Code Challenge Score'].min()} - "
    f"{df['Code Challenge Score'].max()}"
)

print(
    f"Technical Interview Score range: "
    f"{df['Technical Interview Score'].min()} - "
    f"{df['Technical Interview Score'].max()}"
)

print(
    f"Minimum YOE: "
    f"{df['YOE'].min()}"
)

print(
    f"Maximum YOE: "
    f"{df['YOE'].max()}"
)

print(
    f"HIRED candidates: "
    f"{(
        df['Hiring Outcome'] == 'HIRED'
    ).sum()}"
)

print(
    f"NOT HIRED candidates: "
    f"{(
        df['Hiring Outcome'] == 'NOT HIRED'
    ).sum()}"
)

print("=" * 70)
print("PROFILING COMPLETED")
print("=" * 70)