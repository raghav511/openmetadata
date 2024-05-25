import datetime
from airflow import DAG
from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id = 'test_1',
    start_date = datetime.datetime(2024, 1, 1),
    schedule_interval = '@daily'
):
    EmptyOperator(task_id = 'task_1')
