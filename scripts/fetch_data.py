
from pathlib import Path
from datetime import datetime, timezone
import json

import pandas as pd
import requests

BASE_URL = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

OUTPUT = DATA_DIR / "nyc_311_sample.csv"

FIELDS = [
    "unique_key",
    "created_date",
    "closed_date",
    "agency",
    "complaint_type",
    "descriptor",
    "status",
    "borough",
]

PARAMS = {
    "$select": ",".join(FIELDS),
    "$where": (
        "created_date >= '2025-01-01T00:00:00' "
        "AND created_date < '2025-02-01T00:00:00'"
    ),
    "$order": "created_date ASC, unique_key ASC",
    "$limit": 5000,
}

def main():
    print("Connecting to NYC Open Data API...")

    response = requests.get(
        BASE_URL,
        params=PARAMS,
        timeout=90
    )
    response.raise_for_status()

    records = response.json()

    if not records:
        raise ValueError("API returned no records.")

    df = pd.DataFrame(records)

    missing = set(FIELDS) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df = df.reindex(columns=FIELDS)
    df.to_csv(OUTPUT, index=False)

    metadata = {
        "source": BASE_URL,
        "retrieved_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "start_date": "2025-01-01",
        "end_date_exclusive": "2025-02-01",
        "sample_size": len(df),
        "sampling_method": "First 5000 by creation date and ID",
        "request_url": response.url,
    }

    (DATA_DIR / "extract_metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print(f"Downloaded {len(df):,} records")
    print(f"Saved: {OUTPUT}")
    print("\nFirst five rows:")
    print(df.head().to_string(index=False))

    print("\nMissing values:")
    print(df.isna().sum())

if __name__ == "__main__":
    main()
