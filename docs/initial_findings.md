
# QueueWise — Initial Analytical Findings

## Business objective
Identify service categories with potential operational
delays and opportunities for further investigation.

## Dataset
NYC 311 Service Requests (2020–present).

Analysis scope: first 5,000 requests created in
January 2025, ordered by creation timestamp and ID.

## KPI definitions
- Total requests: count of sampled cases
- Closure percentage: share with valid closure timestamps
- Median resolution: typical duration for valid closures
- P90 resolution: 90th percentile duration for valid closures

## Data quality
[Summarise results from quality_report.json]

## Findings
1. [Which category has the longest median duration?]
2. [Which category has the highest P90 duration?]
3. [Which categories have substantial request volumes?]

## Business recommendations
[Recommend areas for investigation, not proven fixes.]

## Limitations
- Non-representative, chronologically selected sample
- Case closure does not necessarily equal issue resolution
- No verified service-level targets
- Differences may reflect service type and complexity
- Historical records may change between API extractions

## Next steps
- Compare agencies and service categories
- Fetch a broader reporting window
- Build an interactive management dashboard
