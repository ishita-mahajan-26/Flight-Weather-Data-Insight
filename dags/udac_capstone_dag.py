from datetime import datetime, timedelta
import datetime
import logging
import os
from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from operators import (StageToRedshiftOperator, LoadFactOperator, LoadDimensionOperator, DataQualityOperator)
from helpers import SqlQueries
from airflow.hooks.S3_hook import S3Hook
from airflow.contrib.hooks.aws_hook import AwsHook
from airflow.hooks.postgres_hook import PostgresHook
import pandas as pd
from pandas.io.json import json_normalize


# /opt/airflow/start.sh
# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime.datetime.utcnow(),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG('udac_capstone_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *'
        )   
 
def preprocess_weather_data():
    logging.info("reading from bucket")
    hook = S3Hook(aws_conn_id='aws_credentials')
    bucket= "udac-flight-weather-dataset"
    prefix1= "Weather/ATL/"
#     s3_file_path = "s3://udac-flight-weather-dataset/Weather/ATL/2016-1.json"
    logging.info(f"Listing Keys from {bucket}/{prefix1}")
    keys = hook.list_keys(bucket, prefix=prefix1)
    
    for key in keys:
        logging.info(f" printing file names")
        logging.info(f"- s3://{bucket}/{key}")
    
    file_content = hook.read_key(
        key='Weather/ATL/2016-1.json',
        bucket_name='udac-flight-weather-dataset')
    
    df_weather = pd.read_json(file_content)
    df_1 = json_normalize(df_weather['data']['weather'])
    df_2 = json_normalize(df_weather['data']['weather'][0]['hourly'])
    logging.info(f" dataframe ready to transform")
    
    location = 'ATL' #taken from file_name
    location = key[8:11]
    df_a = json_normalize(df_weather['data']['weather'])
    no_of_days = len(df_1.index)
    
    date_df = json_normalize(df_weather['data']['weather'])
    required_fields = ["mintempC", "maxtempF", "sunHour", "mintempF", "maxtempC", "date", "uvIndex"]
    datewise_df = date_df[required_fields]
    datewise_df.insert(0, 'location', location)
    hourwise_data_dataframe = pd.DataFrame()
    
    for d in range(no_of_days):
        date_json = df_weather['data']['weather'][d]
        for i in range(0,24):
            hour_df = json_normalize(date_json['hourly'][i])
            fields = ['time', 'tempC', 'date', 'windspeedKmph', 'weather_Desc', 'HeatIndexC', 'visibility', 'weatherCode', 'humidity']
            hour_df['date'] = date_df['date'][d]
            hour_df['weather_Desc'] = hour_df['weatherDesc'][0][0]['value']
            if hourwise_data_dataframe.empty :
                hourwise_data_dataframe = hour_df[fields]
            else:
                hourwise_data_dataframe = pd.concat([hour_df[fields], hourwise_data_dataframe])
                
    # joining the two datasets
    result = pd.merge(datewise_df, hourwise_data_dataframe, on="date")
    logging.info(f" dataframe cols: {result.columns}")
    
    #use this for testing the csv file
    result.to_csv('/home/workspace/airflow/new_downloads/2016-1-ATL.csv', 
                  header=True, 
                  index=False)
    
    hook.load_file("/home/workspace/airflow/new_downloads/2016-1-ATL.csv", 
                   "Weather/result/ATL/2016-1.csv", 
                   bucket_name='udac-flight-weather-dataset'
                  )
    
    logging.info("file saved in s3!")
    

start_operator = DummyOperator(task_id='Begin_execution', dag=dag)

preprocess_data_operator = PythonOperator (
    task_id = 'Preprocessing',
    dag=dag,
    python_callable=preprocess_weather_data
)

stage_flight_data_to_redshift = StageToRedshiftOperator(
    task_id='Stage_flight_data',
    dag=dag,
    table = 'staging_flights',
    redshift_conn_id = 'redshift',
    aws_credentials_id = 'aws_credentials',
    s3_bucket = "udac-flight-weather-dataset",
    s3_key = "Flight/2016/On_Time_On_Time_Performance_2016_1.csv"
)

stage_weather_data_to_redshift = StageToRedshiftOperator(
    task_id='Stage_weather_data',
    dag=dag,
    table = 'staging_weather',
    redshift_conn_id = 'redshift',
    aws_credentials_id = 'aws_credentials',
    s3_bucket = "udac-flight-weather-dataset",
    s3_key = "Weather/result/ATL/2016-1.csv"
)

load_flight_dimension_table = LoadDimensionOperator(
    task_id='Load_flight_dim_table',
    dag=dag,
    table='flight',
    redshift_conn_id="redshift",
    sql=SqlQueries.flight_table_insert
)

load_weather_dimension_table = LoadDimensionOperator(
    task_id='Load_weather_dim_table',
    dag=dag,
    table='weather',
    redshift_conn_id="redshift",
    sql=SqlQueries.weather_table_insert
)

load_location_dimension_table = LoadDimensionOperator(
    task_id='Load_location_dim_table',
    dag=dag,
    table='location',
    redshift_conn_id="redshift",
    sql=SqlQueries.location_table_insert
)

load_flight_weather_fact_table = LoadFactOperator(
    task_id='Load_flight_weather_fact_table',
    dag=dag,
    table='flight_weather',
    redshift_conn_id="redshift",
    sql=SqlQueries.flight_weather_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables = ['location', 'flight', 'weather', 'flight_weather'],
    quality_checks = ['table_exists_check', 'table_contains_records_check']
)

buffer_operator = DummyOperator(task_id='buffer_step',  dag=dag)

end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> preprocess_data_operator >> [stage_flight_data_to_redshift, stage_weather_data_to_redshift ] >> buffer_operator >>[load_flight_dimension_table, load_weather_dimension_table, load_location_dimension_table] >> load_flight_weather_fact_table >> run_quality_checks >> end_operator

