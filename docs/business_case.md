# QueueWise — Business Case

## 1. Executive Summary

QueueWise is a service operations analytics solution that investigates request volume, closure duration and category-level performance using publicly available NYC 311 service request data.

The project combines Python-based data preparation, SQL analysis, Power BI reporting and an interactive Streamlit application.

The objective is to support operational decision-making by making service patterns easier to identify, compare and investigate.

## 2. Business Problem

Service organisations receive requests from different categories, departments and geographical regions.

Without consolidated reporting, operations managers may struggle to identify:

- Categories with unusually long recorded closure durations.
- Categories generating high request volumes.
- Differences in performance across agencies and boroughs.
- Potential areas requiring more detailed investigation.

## 3. Stakeholders (Hypothetical)

| Stakeholder | Business need |
|---|---|
| Operations Director | Understand overall performance and prioritise investigations |
| Service Delivery Manager | Compare closure durations across categories |
| Department Manager | Examine agency-specific workloads |
| Business Analyst | Validate data, identify patterns and communicate findings |
| Data Engineer | Maintain reproducible data extraction and transformation |

These are hypothetical stakeholders for a portfolio case study, not individuals interviewed during the project.

## 4. Business Objectives

1. Provide an accessible view of request volumes and recorded closure durations.
2. Support comparison across agencies, boroughs and categories.
3. Identify patterns that could indicate operational bottlenecks.
4. Provide reproducible analytical outputs for further investigation.

## 5. Solution

QueueWise includes:

- Python extraction from the NYC Open Data API.
- Data quality validation and SQL analytics using DuckDB.
- A Power BI management dashboard.
- A deployed Streamlit application with interactive filters.
- Downloadable category-level analytical summaries.

## 6. Success Criteria

The analytical solution is considered functionally successful when:

- Extracted records have validated identifiers and creation dates.
- Reported KPIs match independently calculated results.
- Dashboard filters correctly update the analysis.
- The public application can be opened without local software installation.
- Data scope, definitions and limitations are documented.

These are product acceptance criteria, not proof of operational improvement.

## 7. Scope and Limitations

The Power BI dashboard currently uses a 5,000-record development sample from January 2025.

The Streamlit application uses a separate historical daily cohort, so its totals should not be expected to match the Power BI development sample.

The analysis does not establish the causes of long closure times, confirm official service-level breaches, or demonstrate actual cost savings.

## 8. Potential Business Value

The solution demonstrates how consolidated operational reporting can help managers identify areas for investigation and establish an analytical basis for improvement initiatives.

Any real performance improvement would require additional stakeholder validation, operational context and measurement after intervention.