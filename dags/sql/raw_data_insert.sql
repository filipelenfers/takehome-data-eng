INSERT INTO raw_current_weather (
     raw_data
) VALUES (
    '{{ ti.xcom_pull(task_ids="ingest_api_data", key="return_value") }}'
);
