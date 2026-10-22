
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="QueueWise | Operations Intelligence",
    page_icon=":bar_chart:",
    layout="wide",
)

DATA = Path(__file__).parent / "data" / "demo_requests.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, dtype={"unique_key": "string"})
    df["resolution_hours"] = pd.to_numeric(
        df["resolution_hours"], errors="coerce"
    )
    df["has_valid_closure"] = (
        df["resolution_hours"].notna()
    )
    return df

st.title("QueueWise")
st.caption("Service Operations Intelligence | NYC 311")
st.info(
    "Historical cohort: requests created on 15 January 2025. "
    "Closure data reflects the time of extraction. "
    "This is a portfolio case study, not an official NYC report."
)

df = load_data()

# SIDEBAR FILTERS
st.sidebar.header("Explore the data")

agency = st.sidebar.multiselect(
    "Agency",
    sorted(df["agency"].dropna().unique()),
)

borough = st.sidebar.multiselect(
    "Borough",
    sorted(df["borough"].dropna().unique()),
)

category = st.sidebar.multiselect(
    "Service Category",
    sorted(df["complaint_type"].dropna().unique()),
)

filtered = df.copy()

if agency:
    filtered = filtered[filtered["agency"].isin(agency)]
if borough:
    filtered = filtered[filtered["borough"].isin(borough)]
if category:
    filtered = filtered[
        filtered["complaint_type"].isin(category)
    ]

# KPI CALCULATIONS
total = filtered["unique_key"].nunique()
valid = filtered["resolution_hours"].dropna()
closed_count = len(valid)

closure_pct = (
    100 * closed_count / total if total else 0
)
median = valid.median() if not valid.empty else None
p90 = valid.quantile(0.9) if not valid.empty else None

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Requests", f"{total:,}")
c2.metric("Recorded Closure %", f"{closure_pct:.1f}%")
c3.metric(
    "Median Closure Hours",
    f"{median:.2f}" if median is not None else "N/A",
)
c4.metric(
    "P90 Closure Hours",
    f"{p90:.2f}" if p90 is not None else "N/A",
)

st.divider()

# CATEGORY ANALYSIS
summary = (
    filtered.groupby("complaint_type", dropna=False)
    .agg(
        requests=("unique_key", "nunique"),
        median_hours=("resolution_hours", "median"),
        valid_closures=("has_valid_closure", "sum"),
    )
    .reset_index()
    .rename(columns={"complaint_type": "Category"})
)

left, right = st.columns(2)

with left:
    st.subheader("Longest Median Closure Times")

    eligible = summary[
        (summary["requests"] >= 20)
        & summary["median_hours"].notna()
    ].nlargest(10, "median_hours")

    if eligible.empty:
        st.warning("No categories meet the 20-request threshold.")
    else:
        fig = px.bar(
            eligible.sort_values("median_hours"),
            x="median_hours",
            y="Category",
            orientation="h",
            hover_data=["requests", "valid_closures"],
            labels={"median_hours": "Median closure hours"},
        )
        st.plotly_chart(fig, width="stretch")

with right:
    st.subheader("Highest Request Volume")

    highest = summary.nlargest(10, "requests")

    if highest.empty:
        st.warning("No requests match the filters.")
    else:
        fig = px.bar(
            highest.sort_values("requests"),
            x="requests",
            y="Category",
            orientation="h",
            labels={"requests": "Number of requests"},
        )
        st.plotly_chart(fig, width="stretch")

# DETAIL TABLE
st.divider()
st.subheader("Category Performance")

st.dataframe(
    summary.sort_values("requests", ascending=False),
    hide_index=True,
    width="stretch",
)

# DOWNLOAD
csv = summary.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download Filtered KPI Report",
    data=csv,
    file_name="queuewise_category_report.csv",
    mime="text/csv",
)

st.divider()

st.caption(
    "Source: NYC Open Data — 311 Service Requests. "
    "Closure times are based only on valid recorded closures. "
    "Long duration does not prove poor agency performance."
)
