from datetime import datetime, timedelta
import time
from airflow import DAG
from airflow.models import Variable
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException, AirflowException, AirflowTaskTimeout
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

ENV = Variable.get('env')
ID = Variable.get('id')

TAGS = ['PythonDataFlow']
DAG_ID = "DAG_FOR_AWS"
DAG_DESCRIPTION = """MI PRIMER DAG_FOR_AWS"""
DAG_SCHEDULE = "0 9 * * *"
default_args = {
    "start_date": datetime(2024, 9, 26),
}
    # retries = 4
    # retry_delay = timedelta(minutes=5)
params = {
    'Manual': False
    # 'Fecha': '2024-09-28'
}

def execute_task (**kwargs):
    print(kwargs)
    params = kwargs.get('params', {})
    manual = params.get('Manual', False)

    # EXCEPTIONS
    if manual:
        raise AirflowException('La tarea a fallado.')
        # raise AirflowSkipException('La tarea a fallado.')

    # if manual:
    #     timeout = 10
    #     start_time = time.time()
    #     while True:
    #         elapsed_time = time.time() - start_time
    #         if elapsed_time > timeout:
    #             raise AirflowTaskTimeout('La tarea ha superado el tiempo de espera')
    #         time.sleep(1)
    #     # raise AirflowException('La tarea ha fallado')
    #     # raise AirflowSkipException('La tarea fue omitida')


    # if manual:
    #     kwargs['ti'].xcom_push(key='color', value='Amarillo')
    # else:
    #     kwargs['ti'].xcom_push(key='color', value='Rojo')

def second_tasks():
    print("Second_task")

# def context_task (**kwargs):
#     ti = kwargs['ti']
#     color = ti.xcom_pull(task_ids='first_task', key='color')
#     print("El color es: ", color) 


# def context_task (ds, color):
#     print("Fecha de ejecución: ", ds) 
#     print("El color es: ", color) 

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
        # trigger_rule=TriggerRule.ALL_SUCCESS,
        # trigger_rule=TriggerRule.ONE_SUCCESS,
        # trigger_rule=TriggerRule.ALL_FAILED,
        # trigger_rule=TriggerRule.ONE_FAILED,
        # trigger_rule=TriggerRule.ALL_DONE,
        trigger_rule=TriggerRule.NONE_FAILED,
    )

    first_task = PythonOperator(
        task_id='first_task',
        python_callable=execute_task,
        # retries=retries,
        # retry_delay=retry_delay,
        # provide_context=True,
    )

    second_task = PythonOperator(
        task_id='second_task',
        python_callable=second_tasks,
        # retries=retries,
        # retry_delay=retry_delay
    )

    # last_task = PythonOperator(
    #     task_id='last_task',
    #     python_callable=context_task,
    #     retries=retries,
    #     retry_delay=retry_delay,
    #     op_kwargs={'ds': '{{ ds }}',
    #                'color': "{{ ti.xcom_pull(task_ids='first_task', key='color') }}"},
    # )


    # second_task = PythonOperator(
    #     task_id='second_task',
    #     python_callable=execute_task,
    #     retries=retries,
    #     retry_delay=retry_delay
    # )

    # third_task = PythonOperator(
    #     task_id='third_task',
    #     python_callable=execute_task,
    #     retries=retries,
    #     retry_delay=retry_delay
    # )

    # four_task = PythonOperator(
    #     task_id='four_task',
    #     python_callable=execute_task,
    #     retries=retries,
    #     retry_delay=retry_delay
    # )

    # five_task = PythonOperator(
    #     task_id='five_task',
    #     python_callable=execute_task,
    #     retries=retries,
    #     retry_delay=retry_delay
    # )

# Establecer dependencias estre tareas
# ************ FORMA 1 ************
# start_task >> first_task >> last_task >> end_task 
# start_task >> first_task >> end_task 
start_task >> [first_task, second_task] >> end_task 
# start_task >> second_task >> end_task 

# ************ FORMA 2 ************
# start_task >> [first_task, second_task] >> third_task
# third_task >> [four_task, five_task] >> end_task




