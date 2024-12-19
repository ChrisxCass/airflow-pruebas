from airflow import DAG
from airflow.decorators import task
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta 
from airflow.operators.python import PythonOperator

dag_owner = 'DAG_POOL'

default_args = {'owner': dag_owner,
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
        }

tablas_info = {
    1: {"message": "Soy la tarea 1"},
    2: {"message": "Soy la tarea 2"},
    3: {"message": "Soy la tarea 3"},
    4: {"message": "Soy la tarea 4"},
    5: {"message": "Soy la tarea 5"}
}

def create_task(message):
    def task_callable(task):
        print(message)
    return task_callable

with DAG(dag_id='DAG_POOL',
        default_args=default_args,
        description='DAG_POOL',
        start_date=datetime(2024,12,16),
        schedule_interval='0 9 * * *',
        catchup=False,
        tags=['DAG_POOL']
):

    start = EmptyOperator(task_id='start')

    end = EmptyOperator(task_id='end')

    # previous_task = start
    for tabla, info in tablas_info.items():
        message = info.get("mesagge")
        python_task = PythonOperator(
            task_id = f"python_task_{tabla}",
            python_callable=create_task(message),
            pool = "My_pool",
        )
        # previous_task >> python_task
        # previous_task = python_task
    
    # python_task >> end
    start >> python_task >> end


    # python_task1 = PythonOperator(
    #     task_id="python_task1",
    #     python_callable=lambda: print('Hi from python operator'),
    #     pool="My_pool"
    # )

    # python_task2 = PythonOperator(
    # task_id="python_task2",
    #     python_callable=lambda: print('Hi from python operator'),
    #     pool="My_pool"
    # )

    # python_task3 = PythonOperator(
    #     task_id="python_task3",
    #     python_callable=lambda: print('Hi from python operator'),
    #     pool="My_pool"
    # )

    # python_task4 = PythonOperator(
    #     task_id="python_task4",
    #     python_callable=lambda: print('Hi from python operator'),
    #     pool="My_pool"
    # )

    # python_task5 = PythonOperator(
    #     task_id="python_task5",
    #     python_callable=lambda: print('Hi from python operator'),
    #     pool="My_pool"
    # )


    # start >> [python_task1, python_task2, python_task3, python_task4, python_task5 ] >> end