"""Clean India EV sales data with pandas and NumPy.

The project is structured for the Kaggle dataset "Electric Vehicle Sales by
State in India". A small dirty sample is included so the pipeline can run
without downloading Kaggle data. Replace the input CSV with the Kaggle export
when available.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "india_ev_sales_sample_dirty.csv"
CLEAN_DATA = ROOT / "data" / "cleaned" / "india_ev_sales_cleaned.csv"
SUMMARY_DATA = ROOT / "outputs" / "state_sales_summary.csv"

MONTH_ALIASES = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}

CATEGORY_ALIASES = {
    "2 wheeler": "2-Wheeler",
    "2-wheeler": "2-Wheeler",
    "3 wheeler": "3-Wheeler",
    "3-wheeler": "3-Wheeler",
    "4 wheeler": "4-Wheeler",
    "4-wheeler": "4-Wheeler",
    "bus": "Bus",
    "goods vehicle": "Goods Vehicle",
}

TYPE_ALIASES = {
    "battery electric": "Battery Electric",
    "plug-in hybrid": "Plug-in Hybrid",
    "plug in hybrid": "Plug-in Hybrid",
}


def _normalize_text(series: pd.Series) -> pd.Series:
    """Trim whitespace, collapse separators, and lowercase text values."""
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"[_\s]+", " ", regex=True)
        .str.lower()
    )


def load_data(path: Path = RAW_DATA) -> pd.DataFrame:
    """Load raw EV sales data from CSV."""
    return pd.read_csv(path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned EV sales dataframe ready for analysis."""
    cleaned = df.copy()
    cleaned.columns = cleaned.columns.str.strip().str.lower().str.replace(" ", "_")

    cleaned["state"] = _normalize_text(cleaned["state"]).str.title()
    cleaned["vehicle_category"] = (
        _normalize_text(cleaned["vehicle_category"]).map(CATEGORY_ALIASES).fillna("Unknown")
    )
    cleaned["vehicle_type"] = (
        _normalize_text(cleaned["vehicle_type"]).map(TYPE_ALIASES).fillna("Unknown")
    )
    cleaned["month"] = _normalize_text(cleaned["month"]).map(MONTH_ALIASES)
    cleaned["year"] = pd.to_numeric(cleaned["year"], errors="coerce").astype("Int64")
    cleaned["sales"] = pd.to_numeric(
        cleaned["sales"].astype("string").str.replace(",", "", regex=False).str.strip(),
        errors="coerce",
    )

    cleaned.loc[cleaned["sales"] < 0, "sales"] = np.nan
    cleaned["sales"] = cleaned.groupby(["state", "vehicle_category"], dropna=False)[
        "sales"
    ].transform(lambda values: values.fillna(values.median()))
    cleaned["sales"] = cleaned["sales"].fillna(cleaned["sales"].median()).round().astype("Int64")

    cleaned = cleaned.drop_duplicates(
        subset=["state", "vehicle_category", "vehicle_type", "year", "month", "sales"]
    )
    cleaned = cleaned.dropna(subset=["state", "year", "month"])
    cleaned["period"] = pd.to_datetime(
        dict(year=cleaned["year"].astype(int), month=cleaned["month"].astype(int), day=1)
    )
    return cleaned.sort_values(["period", "state", "vehicle_category"]).reset_index(drop=True)


def build_state_summary(cleaned: pd.DataFrame) -> pd.DataFrame:
    """Aggregate cleaned sales by Indian state."""
    summary = (
        cleaned.groupby("state", as_index=False)
        .agg(total_sales=("sales", "sum"), records=("sales", "size"))
        .sort_values("total_sales", ascending=False)
    )
    summary["sales_share_pct"] = (summary["total_sales"] / summary["total_sales"].sum() * 100).round(2)
    return summary


def main() -> None:
    """Run the cleaning pipeline and write cleaned datasets."""
    CLEAN_DATA.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY_DATA.parent.mkdir(parents=True, exist_ok=True)

    raw = load_data()
    cleaned = clean_data(raw)
    summary = build_state_summary(cleaned)

    cleaned.to_csv(CLEAN_DATA, index=False)
    summary.to_csv(SUMMARY_DATA, index=False)

    print(f"Cleaned rows: {len(cleaned)}")
    print(f"Cleaned data saved to: {CLEAN_DATA.relative_to(ROOT)}")
    print(f"State summary saved to: {SUMMARY_DATA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
