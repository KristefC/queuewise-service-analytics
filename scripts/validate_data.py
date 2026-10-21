
from pathlib import Path
import json

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "nyc_311_sample.csv"
OUTPUT = ROOT / "data" / "quality_report.json"

REQUIRED = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "complaint_type",
    "status",
]

def validate():
    if not INPUT.exists():
        raise FileNotFoundError(
            f"Dataset not found: {INPUT}. Run fetch_data.py first."
        )

    df = pd.read_csv(INPUT, dtype={"unique_key": "string"})

    missing_columns = [
        col for col in REQUIRED if col not in df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    for col in ["created_date", "closed_date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    elapsed_hours = (
        df["closed_date"] - df["created_date"]
    ).dt.total_seconds() / 3600

    checks = {
        "total_rows": len(df),
        "unique_requests": int(df["unique_key"].nunique()),
        "missing_request_ids": int(df["unique_key"].isna().sum()),
        "duplicate_request_ids": int(
            df["unique_key"].duplicated(keep="first").sum()
        ),
        "invalid_created_dates": int(
            df["created_date"].isna().sum()
        ),
        "missing_or_invalid_closed_dates": int(
            df["closed_date"].isna().sum()
        ),
        "negative_resolution_durations": int(
            (elapsed_hours < 0).sum()
        ),
        "missing_agencies": int(df["agency"].isna().sum()),
        "missing_categories": int(
            df["complaint_type"].isna().sum()
        ),
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(checks, indent=2))

    print("\nQUEUEWISE — DATA QUALITY REPORT")
    print("-" * 42)

    for key, value in checks.items():
        print(f"{key:35} {value}")

    critical_issues = (
        checks["missing_request_ids"]
        + checks["duplicate_request_ids"]
        + checks["invalid_created_dates"]
        + checks["negative_resolution_durations"]
    )

    if critical_issues:
        print("\nWARNING: Critical quality issues detected.")
        print("Review affected records before reporting KPIs.")
    else:
        print("\nCore data-quality checks passed.")

if __name__ == "__main__":
    validate()
