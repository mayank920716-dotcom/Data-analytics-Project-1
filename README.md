# India EV Sales Data Cleaning Project

This repository contains a beginner-friendly Python data cleaning project for Indian electric vehicle (EV) sales by state. It uses **pandas** and **NumPy** to clean, standardize, deduplicate, and summarize EV sales data.

## Dataset reference

The project is designed around the Kaggle dataset **Electric Vehicle Sales by State in India** by `mafzal19`, which is described as state-level Indian EV sales data with vehicle categories and types. The Kaggle page notes that the dataset contains 96,846 rows and 8 columns. Because Kaggle downloads require credentials, this repository includes a small dirty sample CSV that mirrors common fields from the referenced dataset so the pipeline runs immediately.

Reference: <https://www.kaggle.com/datasets/mafzal19/electric-vehicle-sales-by-state-in-india>

## Project structure

```text
.
├── data/
│   ├── raw/india_ev_sales_sample_dirty.csv
│   └── cleaned/india_ev_sales_cleaned.csv
├── outputs/state_sales_summary.csv
├── src/clean_ev_sales.py
├── requirements.txt
└── README.md
```

## Cleaning tasks performed

The script in `src/clean_ev_sales.py` performs the following steps:

1. Loads the raw EV sales CSV with pandas.
2. Standardizes column names to lowercase snake case.
3. Cleans Indian state names with consistent title casing.
4. Normalizes vehicle categories such as `2 wheeler` to `2-Wheeler`.
5. Normalizes vehicle types such as `battery electric` to `Battery Electric`.
6. Converts month names and abbreviations to month numbers.
7. Converts sales values to numeric format after removing commas and whitespace.
8. Uses NumPy-compatible missing-value handling to replace negative sales with missing values.
9. Imputes missing sales using grouped medians, then the overall median as a fallback.
10. Removes duplicate rows and writes cleaned CSV outputs.
11. Builds a state-level sales summary with total sales, record count, and sales share percentage.

## How to run

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the cleaning pipeline:

```bash
python src/clean_ev_sales.py
```

Expected generated files:

- `data/cleaned/india_ev_sales_cleaned.csv`
- `outputs/state_sales_summary.csv`

## Using the full Kaggle dataset

1. Download the CSV from the Kaggle dataset page.
2. Place it in `data/raw/`.
3. Update the `RAW_DATA` path in `src/clean_ev_sales.py` if the filename is different.
4. Run `python src/clean_ev_sales.py`.

If the Kaggle column names differ, update the cleaning script column references to match the downloaded CSV.
