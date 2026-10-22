
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "nyc_311_sample.csv"
OUTPUT = ROOT / "data" / "processed"
OUTPUT.mkdir(parents=True, exist_ok=True)

if not SOURCE.exists():
    raise FileNotFoundError(
        "Run scripts/fetch_data.py first."
    )

con = duckdb.connect()

query = """
WITH typed AS (
    SELECT
        CAST(unique_key AS VARCHAR) AS RequestID,
        COALESCE(
            NULLIF(TRIM(complaint_type), ''),
            'Unknown'
        ) AS Category,
        COALESCE(
            NULLIF(TRIM(agency), ''),
            'Unknown'
        ) AS Agency,
        COALESCE(
            NULLIF(TRIM(status), ''),
            'Unknown'
        ) AS Status,
        COALESCE(
            NULLIF(TRIM(borough), ''),
            'Unknown'
        ) AS Borough,
        TRY_CAST(created_date AS TIMESTAMP) AS CreatedAt,
        TRY_CAST(closed_date AS TIMESTAMP) AS ClosedAt
    FROM read_csv_auto(?, all_varchar = true)
),
validated AS (
    SELECT *,
        CASE
            WHEN CreatedAt IS NOT NULL
             AND ClosedAt IS NOT NULL
             AND ClosedAt >= CreatedAt
            THEN 1 ELSE 0
        END AS HasValidClosure
    FROM typed
)
SELECT
    RequestID,
    Category,
    Agency,
    Status,
    Borough,
    CreatedAt,
    ClosedAt,
    HasValidClosure,
    CASE
        WHEN HasValidClosure = 1
        THEN ROUND(
            DATE_DIFF(
                'second', CreatedAt, ClosedAt
            ) / 3600.0, 2
        )
        ELSE NULL
    END AS ResolutionHours
FROM validated
"""

fact = con.execute(query, [str(SOURCE)]).df()
con.close()

# Reject invalid case identifiers and duplicate IDs.
# We do not silently delete potentially conflicting rows.
if fact["RequestID"].isna().any():
    raise ValueError("Missing request IDs detected.")

if fact["RequestID"].duplicated().any():
    raise ValueError("Duplicate request IDs detected.")

if fact["CreatedAt"].isna().any():
    raise ValueError("Invalid creation dates detected.")

if fact.empty:
    raise ValueError("No valid records found.")

categories = (
    fact[["Category"]]
    .drop_duplicates()
    .sort_values("Category")
    .reset_index(drop=True)
)
categories["CategoryGroup"] = "Service Operations"

fact.to_csv(
    OUTPUT / "fact_requests.csv",
    index=False
)

categories.to_csv(
    OUTPUT / "dim_category.csv",
    index=False
)

print("\nQUEUEWISE — ANALYTICAL MODEL")
print("-" * 40)
print(f"Fact rows: {len(fact):,}")
print(f"Categories: {len(categories)}")
print(
    "Valid recorded closures:",
    int(fact["HasValidClosure"].sum())
)
print(
    "Missing/invalid closures:",
    int((fact["HasValidClosure"] == 0).sum())
)
print("\nFiles saved in data/processed/")
