from datetime import datetime, timedelta
import time
from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException, AirflowException, AirflowTaskTimeout
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.operators.s3 import S3CopyObjectOperator

ENV = Variable.get('env')
ID = Variable.get('id')

TAGS = ['PythonDataFlow']
DAG_ID = "MI_PRIMER_DAG"
DAG_DESCRIPTION = """MI PRIMER DAG DE PRUEBA"""
DAG_SCHEDULE = "0 9 * * *"
default_args = {
    "start_date": datetime(2024, 9, 26),
}
bucket_key = "pruebas/prueba.txt"
bucket_name = "mybucketforairflow"
dest_bucket_key = "prueba_copy/Prueba.txt"
dest_bucket_name = "copy-airflow-prueba"

params = {
    'Manual': False
}

def execute_task (**kwargs):
    print(kwargs)
    params = kwargs.get('params', {})
    manual = params.get('Manual', False)

    # EXCEPTIONS
    if manual:
        raise AirflowException('La tarea a fallado.')

def second_tasks():
    print("Second_task")

dag = DAG(
    dag_id=DAG_ID,
    description=DAG_DESCRIPTION,
    catchup=False,
    schedule_interval=DAG_SCHEDULE,
    max_active_runs=1,
    dagrun_timeout=timedelta(seconds=200000),
    default_args=default_args,
    tags=TAGS,
    params = params
)

with dag as dag:
    start_task = EmptyOperator(
        task_id='inicia_proceso'
    )

    end_task = EmptyOperator(
        task_id='finaliza_proceso',
        trigger_rule=TriggerRule.NONE_FAILED,
    )

    # from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
    S3KeySensor_sensor = S3KeySensor(
        task_id='S3KeySensor_sensor',   
        bucket_key=bucket_key,
        bucket_name=bucket_name,
        wildcard_match=False,
        check_fn=None,
        aws_conn_id='aws_default',
        verify=None,
        )

    S3CopyObjectOperator_task = S3CopyObjectOperator(
        task_id='S3CopyObjectOperator_task',
        source_bucket_key=bucket_key,
        source_bucket_name=bucket_name,
        dest_bucket_key=dest_bucket_key,
        dest_bucket_name=dest_bucket_name,
        source_version_id=None,
        aws_conn_id='aws_default',
        verify=None,
        acl_policy=None,
        )


# ************ EJECUCIÓN ************
start_task >> S3KeySensor_sensor >> S3CopyObjectOperator_task  >> end_task 




