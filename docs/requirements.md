
# QueueWise — Business Requirements

## Stakeholder Requirements

| ID | Requirement | Priority |
|---|---|---|
| BR-01 | View overall request performance | Must |
| BR-02 | Compare service category performance | Must |
| BR-03 | Filter by agency and borough | Must |
| BR-04 | Identify high-volume categories | Must |
| BR-05 | Investigate long closure durations | Must |
| BR-06 | Download analysis results | Should |

## Functional Requirements

FR-01: The application shall display request count,
recorded closure percentage, median duration and P90.

FR-02: Users shall filter by agency, borough and
service category.

FR-03: Users shall see the ten highest-volume categories.

FR-04: Users shall see categories ranked by median
closure duration, excluding groups below a documented
minimum sample size.

FR-05: Users shall be able to download a category
performance report.

## Non-Functional Requirements

NFR-01: KPI calculations must be consistent within
the same reporting dataset and filter context.

NFR-02: Invalid timestamps must not contribute to
resolution-duration calculations.

NFR-03: The application must display its data source,
reporting scope and limitations.

NFR-04: Source extraction must be reproducible
from documented scripts and parameters.

## Acceptance Criteria

AC-01: Unfiltered request counts match the
validated source dataset.

AC-02: Selecting one category updates all KPI cards.

AC-03: Empty filters do not cause application errors.

AC-04: Downloaded results reflect the selected filters.

AC-05: Public users can open the deployed app.

## KPI Definitions

Total Requests:
Count of unique service request identifiers.

Recorded Closure %:
Valid recorded closures / total sampled requests.

Median Closure Hours:
Median nonnegative duration between creation
and recorded closure timestamps.

P90 Closure Hours:
90th percentile of valid closure durations.

Category Volume:
Count of sampled requests in each category.

Important:
The closure percentage is not an official NYC SLA
compliance measure.
