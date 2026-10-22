
import pandas as pd
import pytest


def calculate_kpis(df):
    total = df["unique_key"].nunique()
    valid = pd.to_numeric(
        df["resolution_hours"], errors="coerce"
    ).dropna()

    return {
        "total": total,
        "valid_closures": len(valid),
        "closure_rate": len(valid) / total if total else 0,
        "median": valid.median(),
        "p90": valid.quantile(0.9),
    }


def test_kpi_calculations():
    sample = pd.DataFrame({
        "unique_key": ["1", "2", "3", "4"],
        "resolution_hours": [2.0, 4.0, 6.0, None],
    })

    result = calculate_kpis(sample)

    assert result["total"] == 4
    assert result["valid_closures"] == 3
    assert result["closure_rate"] == pytest.approx(0.75)
    assert result["median"] == pytest.approx(4.0)
    assert result["p90"] == pytest.approx(5.6)


def test_empty_data():
    sample = pd.DataFrame({
        "unique_key": pd.Series(dtype="string"),
        "resolution_hours": pd.Series(dtype="float"),
    })

    result = calculate_kpis(sample)

    assert result["total"] == 0
    assert result["closure_rate"] == 0
