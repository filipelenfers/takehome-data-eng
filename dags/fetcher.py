from datetime import datetime, timedelta
import time
import urllib.request
import json

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG
from airflow.models import Variable

# Operators; we need this to operate!
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
        'fetcher',
        default_args=default_args,
        description='To fetch the weather data',
        schedule_interval=timedelta(minutes=5),
        start_date=datetime(2021, 1, 1),
        catchup=False,
        tags=['take-home'],
) as dag:
    
    def get_weather_data(city:str, country_code:str, api_key:str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&units=metric&appid={api_key}"
        result = json.load(urllib.request.urlopen(url))
        #result['weather'] = json.dumps(result['weather']) if 'weather' in result else '[]'
        result = json.dumps(result)
        return result


    t1 = PythonOperator(
        task_id='ingest_api_data',
        python_callable=get_weather_data,
        op_kwargs={'city': Variable.get('openweather_city'), 'country_code': Variable.get('openweather_country'), 'api_key': Variable.get("openweather_api_key") },
    )

    # Create a table to store the raw data
    t2 = PostgresOperator(
        task_id="create_raw_dataset",
        sql="sql/create_raw_data_table.sql",
    )

    t3 = PostgresOperator(
        task_id="store_dataset",
        sql="sql/raw_data_insert.sql",
    )

    t1 >> t2 >> t3