from datetime import datetime, timedelta
import time
import urllib.request
import json

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

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

    # @TODO: Add your function here. Example here: https://airflow.apache.org/docs/apache-airflow/stable/_modules/airflow/example_dags/example_python_operator.html
    # Hint: How to fetch the weather data from OpenWeatherMap?
    def my_sleeping_function(random_base):
        """This is a function that will run within the DAG execution"""
        time.sleep(random_base)
    
    def get_weather_data(city:str, country_code:str, api_key:str):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&units=metric&appid={api_key}"
        result = json.load(urllib.request.urlopen(url))
        result['weather'] = json.dumps(result['weather']) if 'weather' in result else '[]'
        return result


    t1 = PythonOperator(
        task_id='ingest_api_data',
        python_callable=get_weather_data,
        op_kwargs={'city': 'vancouver', 'country_code': 'ca', 'api_key': '3a7100422018837ce9983e795878384b'}, #TODO get from variables
    )

    # Create a table to store the raw data
    t2 = PostgresOperator(
        task_id="create_raw_dataset",
        sql="create_raw_data_table.sql",
    )

    t3 = PostgresOperator(
        task_id="store_dataset",
        sql="raw_data_insert.sql",
    )

    t1 >> t2 >> t3