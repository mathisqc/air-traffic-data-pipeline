{{ config(materialized='table') }}

SELECT
    DATA:icao24::STRING AS icao24,
    DATA:callsign::STRING AS callsign,
    DATA:origin_country::STRING AS origin_country,

    DATA:time_position::TIMESTAMP_TZ AS time_position,
    DATA:last_contact::TIMESTAMP_TZ AS last_contact,
    DATA:snapshot_time::TIMESTAMP_TZ AS snapshot_time,

    DATA:longitude::FLOAT AS longitude,
    DATA:latitude::FLOAT AS latitude,
    DATA:baro_altitude::FLOAT AS baro_altitude,
    DATA:geo_altitude::FLOAT AS geo_altitude,

    DATA:on_ground::BOOLEAN AS on_ground,
    DATA:velocity::FLOAT AS velocity,
    DATA:true_track::FLOAT AS true_track,
    DATA:vertical_rate::FLOAT AS vertical_rate,

    DATA:squawk::STRING AS squawk,
    DATA:spi::BOOLEAN AS spi,
    DATA:position_source::INTEGER AS position_source,

    DATA:velocity_suspicious::BOOLEAN AS velocity_suspicious,
    DATA:baro_altitude_suspicious::BOOLEAN AS baro_altitude_suspicious,
    DATA:geo_altitude_suspicious::BOOLEAN AS geo_altitude_suspicious,
    DATA:vertical_rate_suspicious::BOOLEAN AS vertical_rate_suspicious

FROM AIR_TRAFFIC_DB.RAW.OPENSKY_RAW
