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

# /opt/airflow/start.sh
# AWS_KEY = os.environ.get('AWS_KEY')
# AWS_SECRET = os.environ.get('AWS_SECRET')

default_args = {
    'owner': 'udacity',
    'start_date': datetime.datetime.utcnow(),
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False

}

dag = DAG('udac_example_dag',
          default_args=default_args,
          description='Load and transform data in Redshift with Airflow',
          schedule_interval='0 * * * *',
          catchup= False
        )

def list_keys():
    hook = S3Hook(aws_conn_id='aws_credentials')
    bucket = Variable.get('s3_bucket')
    prefix = Variable.get('s3_bucket_prefix_log')
    logging.info(f"Listing Keys from {bucket}/{prefix}")
    keys = hook.list_keys(bucket, prefix=prefix)
    for key in keys:
        logging.info(f"- s3://{bucket}/{key}")        

start_operator = DummyOperator(task_id='Begin_execution',  dag=dag)

# list_objects_task = PythonOperator(task_id="list_keys", python_callable=list_keys, dag=dag)

# create_staging_events_task = PostgresOperator(
#     task_id="create_staging_events_tables_in_redshift_dummy_task",
#     dag=dag,
#     postgres_conn_id="redshift",
#     sql='''
#     CREATE TABLE public.dummy_staging_events_3(
# 	artist varchar(256),
# 	auth varchar(256),
# 	firstname varchar(256),
# 	gender varchar(256),
# 	iteminsession int4,
# 	lastname varchar(256),
# 	length numeric(18,0),
# 	"level" varchar(256),
# 	location varchar(256),
# 	"method" varchar(256),
# 	page varchar(256),
# 	registration numeric(18,0),
# 	sessionid int4,
# 	song varchar(256),
# 	status int4,
# 	ts int8,
# 	useragent varchar(256),
# 	userid int4
#     );
#     '''
# )



# def load_data_to_redshift(*args, **kwargs):
#     aws_hook = AwsHook(aws_conn_id='aws_credentials')
#     credentials = aws_hook.get_credentials()
#     redshift_hook = PostgresHook("redshift")
#     test_file_path = 's3://udacity-dend/log-data/2018/11/2018-11-10-events.json'
#     destination_table_name = 'dummy_staging_events_1'
#     sql = """
#         COPY {}
#         FROM '{}'
#         ACCESS_KEY_ID '{}'
#         SECRET_ACCESS_KEY '{}'
#         JSON 'auto'
#         """
#     redshift_hook.run(sql.format(destination_table_name, test_file_path, credentials.access_key, credentials.secret_key))

# copy_data_task = PythonOperator(
#     task_id='load_from_s3_to_redshift',
#     dag=dag,
#     python_callable=load_data_to_redshift
# )


# stage_events_to_redshift = StageToRedshiftOperator(
#     task_id='Stage_events',
#     dag=dag,
#     table = 'staging_events',
#     redshift_conn_id = 'redshift',
#     aws_credentials_id = 'aws_credentials',
#     s3_bucket = "udacity-dend",
#     s3_key = "log_data",
#     json_path = "s3://udacity-dend/log_json_path.json",
#     file_type = "json",
#     region = "us-west-2"
# )

# start_operator >> list_objects_task >> create_staging_events_task >> copy_data_task >> stage_events_to_redshift



# stage_songs_to_redshift = StageToRedshiftOperator(
#     task_id='Stage_songs',
#     dag=dag,
#     table="staging_songs",
#     redshift_conn_id="redshift",
#     aws_credentials_id="aws_credentials",
#     s3_bucket="udacity-dend",
#     s3_key = "song_data/A/A/A",
#     json_path="auto",
#     file_type = "json",
#     region = "us-west-2"
# )

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    table='songplays',
    redshift_conn_id="redshift",
    sql=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    table='user',
    redshift_conn_id="redshift",
    sql=SqlQueries.user_table_insert
)


end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

start_operator >> load_songplays_table >> load_user_dimension_table >> end_operator

# start_operator >> list_objects_task >> [create_staging_events_task, create_staging_songs_task] >> [stage_events_to_redshift, stage_songs_to_redshift] >> end_operator




# load_song_dimension_table = LoadDimensionOperator(
#     task_id='Load_song_dim_table',
#     dag=dag,
#     table='song',
#     redshift_conn_id="redshift",
#     sql=SqlQueries.song_table_insert
# )

# load_artist_dimension_table = LoadDimensionOperator(
#     task_id='Load_artist_dim_table',
#     dag=dag,
#     table='artist',
#     redshift_conn_id="redshift",
#     sql=SqlQueries.artist_table_insert
# )

# load_time_dimension_table = LoadDimensionOperator(
#     task_id='Load_time_dim_table',
#     dag=dag,
#     table='time',
#     redshift_conn_id="redshift",
#     sql=SqlQueries.time_table_insert
# )

# run_quality_checks = DataQualityOperator(
#     task_id='Run_data_quality_checks',
#     dag=dag
# )

# end_operator = DummyOperator(task_id='Stop_execution',  dag=dag)

# start_operator >> [stage_events_to_redshift, stage_songs_to_redshift] >> load_songplays_table >> [load_user_dimension_table, load_song_dimension_table, load_artist_dimension_table, load_time_dimension_table] >> run_quality_checks >> end_operator