{{ config(materialized='view') }}

SELECT
    *,
    ROUND(velocity * 3.6, 0) AS velocity_kmh,

    CASE
        WHEN baro_altitude < 2000 THEN '< 2,000 m'
        WHEN baro_altitude < 6000 THEN '2,000 - 6,000 m'
        WHEN baro_altitude < 10000 THEN '6,000 - 10,000 m'
        WHEN baro_altitude <= 14000 THEN '10,000 - 14,000 m'
        ELSE '> 14,000 m (Suspicious)'
    END AS altitude_band,

    CASE
        WHEN velocity_suspicious
        OR baro_altitude_suspicious
        OR geo_altitude_suspicious
        OR vertical_rate_suspicious
        THEN TRUE
        ELSE FALSE
    END AS is_suspicious


FROM {{ ref('stg_opensky') }}
WHERE snapshot_time = (
    SELECT MAX(snapshot_time)
    FROM {{ ref('stg_opensky') }}
)
