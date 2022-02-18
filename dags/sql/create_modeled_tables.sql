/*
Table to the fields from raw weather data expanded to faciliate queries.
*/
CREATE TABLE IF NOT EXISTS current_weather (
    id integer primary key,
    ingestion_timestamp_utc timestamp without time zone,
    datetime_utc timestamp  without time zone,
    city_name varchar(255),
    city_id integer,
    timezone_offset integer,
    datetime_local timestamp without time zone,
    latitude decimal(9, 6),
    longitude decimal(9, 6),
    base varchar(255),
    main_temp_c decimal(5, 2),
    main_feels_like_c decimal(5, 2),
    main_pressure_hpa integer,
    main_humidity integer,
    main_temp_min_c decimal(5, 2),
    main_temp_max_c decimal(5, 2),
    main_sea_level_hpa integer,
    main_grnd_level_hpa integer,
    wind_speed_m_s decimal(9, 2),
    wind_deg decimal(9, 2),
    wind_gust_m_s decimal(9, 2),
    clouds_all decimal(9, 2),
    rain_1h_mm decimal(9, 2),
    rain_3h_mm decimal(9, 2),
    snow_1h_mm decimal(9, 2),
    snow_3h_mm decimal(9, 2),
    sys_type integer,
    sys_id integer,
    sys_message varchar(255),
    sys_country varchar(255),
    sys_sunrise_utc timestamp without time zone,
    sys_sunset_utc timestamp without time zone,
    sys_sunrise_local timestamp without time zone,
    sys_sunset_local timestamp without time zone,
    cod integer,
    etl_timestamp_utc timestamp without time zone default (now() at time zone 'utc')
);

/*
Table to keep the unested weather conditions array.
*/
CREATE TABLE IF NOT EXISTS current_weather_conditions (
    id integer primary key,
    ingestion_timestamp_utc timestamp without time zone,
    weather_id int,
    main varchar(255),
    description varchar(255),
    icon varchar(255),
   etl_timestamp_utc timestamp without time zone default (now() at time zone 'utc')
);