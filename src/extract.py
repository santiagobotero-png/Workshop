from pathlib import Path
import pandas as pd


# Ruta raíz del proyecto
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Ruta del archivo fuente
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "candidates.csv"


def extract_data():
    """
    Extract the source data from the CSV file.

    The original source file is preserved and no business
    transformations are performed during extraction.
    """

    df = pd.read_csv(
        DATA_PATH,
        sep=";"
    )

    return df


if __name__ == "__main__":
    df = extract_data()

    print("EXTRACTION COMPLETED")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 records:")
    print(df.head())