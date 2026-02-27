import pandas as pd
from pathlib import Path


def generate_summary(df: pd.DataFrame) -> str:
    total_rows = len(df)
    total_revenue = df["amount"].sum()
    avg_revenue = df["amount"].mean()
    top_city = df["city"].value_counts().idxmax()
    missing_email = df["email"].isna().sum()

    summary = f"""
DATA SUMMARY REPORT
-------------------
Total Rows: {total_rows}
Total Revenue: {total_revenue:.2f}
Average Revenue: {avg_revenue:.2f}
Top City: {top_city}
Missing Emails: {missing_email}
"""

    return summary


def save_summary(summary: str, output_path: Path):
    with open(output_path, "w") as f:
        f.write(summary)


if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    input_file = BASE_DIR / "output" / "cleaned_sales.csv"
    output_file = BASE_DIR / "output" / "summary.txt"

    df = pd.read_csv(input_file)
    report = generate_summary(df)
    save_summary(report, output_file)

    print("Summary report generated successfully.")