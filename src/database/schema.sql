-- Create the daily weather table if it does not already exist.
CREATE TABLE IF NOT EXISTS daily_weather (
    -- City identifies where the weather was recorded.
    city TEXT NOT NULL,

    -- DATE stores the observation date without a time component.
    date DATE NOT NULL,

    -- Weather measurements can contain decimal values.
    temperature_2m_mean DOUBLE PRECISION,
    temperature_2m_max DOUBLE PRECISION,
    temperature_2m_min DOUBLE PRECISION,
    precipitation_sum DOUBLE PRECISION,
    wind_speed_10m_max DOUBLE PRECISION,

    -- Weather codes are whole numbers.
    weather_code INTEGER,

    -- Store the ingestion timestamp with timezone information.
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- A city can have only one record for each date.
    CONSTRAINT daily_weather_city_date_unique
        UNIQUE (city, date)
);
