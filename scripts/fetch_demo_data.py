
from pathlib import Path
from datetime import datetime, timezone
import json
import time

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "app" / "data" / "demo_requests.csv"
METADATA = ROOT / "app" / "data" / "demo_metadata.json"

API = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"

FIELDS = [
    "unique_key", "created_date", "closed_date",
    "agency", "complaint_type", "status", "borough"
]

START = "2025-01-15T00:00:00"
END = "2025-01-16T00:00:00"
PAGE_SIZE = 1000
MAX_ROWS = 50000

def main():
    records = []
    offset = 0

    with requests.Session() as session:
        while True:
            params = {
                "$select": ",".join(FIELDS),
                "$where": (
                    f"created_date >= '{START}' "
                    f"AND created_date < '{END}'"
                ),
                "$order": "created_date ASC, unique_key ASC",
                "$limit": PAGE_SIZE,
                "$offset": offset,
            }

            for attempt in range(3):
                try:
                    response = session.get(
                        API, params=params, timeout=60
                    )
                    response.raise_for_status()
                    break
                except requests.RequestException:
                    if attempt == 2:
                        raise
                    time.sleep(2 ** attempt)

            page = response.json()
            records.extend(page)

            print(f"Downloaded {len(records):,} rows")

            if len(records) > MAX_ROWS:
                raise RuntimeError(
                    "Daily cohort exceeds safety limit. "
                    "Choose a smaller reporting window."
                )

            if len(page) < PAGE_SIZE:
                break

            offset += PAGE_SIZE

    if not records:
        raise RuntimeError("API returned no records.")

    df = pd.DataFrame(records).reindex(columns=FIELDS)

    if df["unique_key"].isna().any():
        raise ValueError("Request IDs are missing.")

    if df["unique_key"].duplicated().any():
        raise ValueError("Duplicate request IDs detected.")

    created = pd.to_datetime(
        df["created_date"], errors="coerce"
    )
    closed = pd.to_datetime(
        df["closed_date"], errors="coerce"
    )

    if created.isna().any():
        raise ValueError("Invalid creation timestamps.")

    duration = (closed - created).dt.total_seconds() / 3600

    df["resolution_hours"] = duration.where(duration >= 0)
    df["has_valid_closure"] = df["resolution_hours"].notna()

    for col in ["agency", "complaint_type", "borough"]:
        df[col] = df[col].fillna("Unknown").replace("", "Unknown")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT, index=False)

    metadata = {
        "source": API,
        "cohort_start": START,
        "cohort_end_exclusive": END,
        "retrieved_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "rows": len(df),
        "scope": "Complete daily creation cohort at extraction time",
    }

    METADATA.write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    print(f"\nSaved {len(df):,} requests to {OUTPUT}")
    print(
        "Valid closures:",
        int(df["has_valid_closure"].sum())
    )
    print(
        "Median closure hours:",
        round(df["resolution_hours"].median(), 2)
    )

if __name__ == "__main__":
    main()
