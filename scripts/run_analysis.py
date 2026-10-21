
from pathlib import Path

import duckdb
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SQL_FILE = ROOT / "sql" / "01_service_kpis.sql"
OUTPUT = ROOT / "data" / "category_kpis.csv"

def main():
    query = SQL_FILE.read_text(encoding="utf-8")

    connection = duckdb.connect(database=":memory:")

    try:
        # Resolve relative CSV paths used by the SQL query.
        import os
        original_directory = Path.cwd()
        os.chdir(ROOT)

        try:
            results = connection.execute(query).df()
        finally:
            os.chdir(original_directory)
    finally:
        connection.close()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT, index=False)

    print("\nQUEUEWISE — SERVICE CATEGORY ANALYSIS")
    print("=" * 55)

    if results.empty:
        print("No categories meet the minimum sample size.")
        return

    print(results.head(10).to_string(index=False))
    print(f"\nCategories analysed: {len(results)}")
    print(f"Output saved to: {OUTPUT}")

if __name__ == "__main__":
    main()
