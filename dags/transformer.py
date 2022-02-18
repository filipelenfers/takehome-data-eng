from datetime import datetime, timedelta

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.providers.postgres.operators.postgres import PostgresOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}
with DAG(
        'transformer',
        default_args=default_args,
        description='To transform the raw current weather to a modeled dataset',
        schedule_interval=timedelta(minutes=5),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=['take-home'],
) as dag:

    t1 = PostgresOperator(
        task_id="create_modeled_dataset_table",
        sql="sql/create_modeled_tables.sql",
    )

    t2 = PostgresOperator(
        task_id="transform_raw_into_current_weather",
        sql="sql/current_weather_insert.sql",
    )

    t3 = PostgresOperator(
        task_id="transform_raw_into_current_weather_conditions",
        sql="sql/current_weather_conditions_insert.sql",
    )

    t1 >> t2 >> t3