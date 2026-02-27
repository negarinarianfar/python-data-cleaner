import pandas as pd
from pathlib import Path


def load_data(file_path: Path) -> pd.DataFrame:
    """Load csv file into DataFrame."""
    return pd.read_csv(file_path)


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw sales data."""

    # Remove duplicates
    df = df.drop_duplicates().copy()


    # Strip whitespace from text columns
    text_columns = ["customer_name", "email", "city", "category"]
    for col in text_columns:
        df[col] = df[col].astype(str).str.strip()

    # Standardize city (lowercase then capitalize)
    df.loc[:, "city"] = df["city"].str.lower().str.capitalize()
    # Convert date to datetime
    df.loc[:, "date"] = pd.to_datetime(df["date"], errors="coerce")

    df.loc[:, "amount"] = pd.to_numeric(df["amount"], errors="coerce").astype("Float64")
    median_amount = df["amount"].median()
    print(df["amount"].dtype)
    print(df["amount"].head(10))
    df.loc[:, "amount"] = df["amount"].fillna(median_amount)


    # Fill missing values
    df.loc[:, "email"] = df["email"].fillna("unknown@email.com")
    df["amount"].isna().sum()

    return df


def save_cleaned(df: pd.DataFrame, output_path: str):
    """Save cleaned data."""
    df.to_csv(output_path, index=False)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    input_file = BASE_DIR / "data" / "raw_sales.csv"
    output_file = BASE_DIR / "output" / "cleaned_sales.csv"

    df_raw = load_data(input_file)
    df_clean = clean_dataframe(df_raw)
    save_cleaned(df_clean, output_file)

    print("Data cleaned and saved successfully.")