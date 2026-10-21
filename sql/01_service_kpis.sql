
-- QUEUEWISE: SERVICE CATEGORY PERFORMANCE
-- Source: NYC 311 sampled service requests
-- Grain: one row per complaint_type
-- Note: results describe the extracted sample only.

WITH cleaned AS (
    SELECT
        unique_key,
        agency,
        complaint_type,
        status,

        TRY_CAST(created_date AS TIMESTAMP) AS created_at,
        TRY_CAST(closed_date AS TIMESTAMP) AS closed_at

    FROM read_csv_auto('data/nyc_311_sample.csv',
                       all_varchar = true)
),

case_metrics AS (
    SELECT
        unique_key,
        COALESCE(complaint_type, 'Unknown') AS service_category,
        agency,
        status,
        created_at,
        closed_at,

        CASE
            WHEN created_at IS NOT NULL
             AND closed_at IS NOT NULL
             AND closed_at >= created_at
            THEN DATE_DIFF('second', created_at, closed_at) / 3600.0
            ELSE NULL
        END AS resolution_hours

    FROM cleaned
    WHERE unique_key IS NOT NULL
      AND created_at IS NOT NULL
),

category_kpis AS (
    SELECT
        service_category,

        COUNT(*) AS total_requests,

        COUNT(resolution_hours) AS valid_closed_requests,

        ROUND(
            100.0 * COUNT(resolution_hours) / COUNT(*),
            2
        ) AS recorded_closure_pct,

        ROUND(
            MEDIAN(resolution_hours),
            2
        ) AS median_resolution_hours,

        ROUND(
            QUANTILE_CONT(resolution_hours, 0.90),
            2
        ) AS p90_resolution_hours,

        ROUND(
            AVG(resolution_hours),
            2
        ) AS avg_resolution_hours

    FROM case_metrics
    GROUP BY service_category
)

SELECT *
FROM category_kpis

-- Avoid ranking categories containing only a few cases.
WHERE total_requests >= 20

ORDER BY median_resolution_hours DESC NULLS LAST;
