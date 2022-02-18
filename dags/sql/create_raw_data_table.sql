CREATE TABLE IF NOT EXISTS raw_current_weather (
     id integer primary key generated always as identity,
     ingestion_timestamp_utc timestamp without time zone default (now() at time zone 'utc'),
     raw_data jsonb
);
