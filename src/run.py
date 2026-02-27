import argparse
from pathlib import Path
import pandas as pd

from clean import clean_dataframe


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def generate_summary(df: pd.DataFrame) -> str:
    total_rows = len(df)
    total_revenue = df["amount"].sum()
    avg_revenue = df["amount"].mean()
    top_city = df["city"].value_counts().idxmax() if "city" in df.columns and not df["city"].empty else "N/A"
    missing_email = df["email"].isna().sum() if "email" in df.columns else "N/A"

    summary = f"""
DATA SUMMARY REPORT
-------------------
Total Rows: {total_rows}
Total Revenue: {total_revenue:.2f}
Average Revenue: {avg_revenue:.2f}
Top City: {top_city}
Missing Emails: {missing_email}
"""
    return summary.strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Clean CSV data and generate a summary report.")
    parser.add_argument("--input", required=True, help="Path to input CSV file (e.g. data/raw_sales.csv)")
    parser.add_argument("--outdir", default="output", help="Output directory (default: output)")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent.parent
    input_path = (base_dir / args.input).resolve() if not Path(args.input).is_absolute() else Path(args.input)
    outdir = (base_dir / args.outdir).resolve() if not Path(args.outdir).is_absolute() else Path(args.outdir)

    ensure_dir(outdir)

    # Load
    df_raw = pd.read_csv(input_path)

    # Clean
    df_clean = clean_dataframe(df_raw)

    # Save cleaned
    cleaned_path = outdir / "cleaned_sales.csv"
    df_clean.to_csv(cleaned_path, index=False)

    # Summary
    summary_text = generate_summary(df_clean)
    summary_path = outdir / "summary.txt"
    summary_path.write_text(summary_text, encoding="utf-8")

    print(f"✅ Cleaned file saved: {cleaned_path}")
    print(f"✅ Summary saved: {summary_path}")


if __name__ == "__main__":
    main()