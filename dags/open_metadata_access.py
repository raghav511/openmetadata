import requests
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    dag_id='open_metadata_access',
    default_args=default_args,
    description='A simple tutorial DAG',
    schedule_interval='@daily'
)


token = 'eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6ImluZ2VzdGlvbi1ib3QiLCJyb2xlcyI6WyJJbmdlc3Rpb25Cb3RSb2xlIl0sImVtYWlsIjoiaW5nZXN0aW9uLWJvdEBvcGVubWV0YWRhdGEub3JnIiwiaXNCb3QiOnRydWUsInRva2VuVHlwZSI6IkJPVCIsImlhdCI6MTcxNjU5ODYzMSwiZXhwIjpudWxsfQ.QBZvk74pVR05DIhVri0J64a16JqtZBRYjo02uUHuwoObZybIMbdfao0dwOxPTaFhXhP93c7nH7f76sWhXFbpJhOFEgVlXE1I2i_x3euGNBvyS9vPsGsNH-MKxOIgea_3ENPtCZ96FT8-n1FTOdptJ7Bdxk9PdHlcrgBt8VYbCn2xvDX-yNA5_sVO9X4DXYz7lq12_usk_19APIUYR068WB8NpSkjsdtlMSCfDNjOUuFXt-8FL5-520olOcsjTt_lZK8JQldA-6fF_wzfTYHAi7s--3XeYAuRmnugsWNp7pXzfgOmUHHcECk46mASrQ4fYr6l3VUgb8xnMdm4aULl3Q'
headers = {'Authorization': f'Bearer {token}'}


def list_db():
    url = "http://openmetadata_server:8585/api/v1/databases"
    params = {'fields': 'owner'}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print('Connection successful!')
    else:
        print('Connection failed!')
    print('Status code:', response.status_code)
    # print('Response:', response.json())
    print(response.json())


def create_db():
    url = "http://openmetadata_server:8585/api/v1/databases"
    request_body = {'name': 'test_db_260524',
                    'service': 'raghav_snowflake'}
    response = requests.post(url, headers=headers, json=request_body)
    if response.status_code == 200:
        print('database created')
    else:
        print('Connection failed!', response.status_code)


def list_app():
    url = "http://openmetadata_server:8585/api/v1/apps"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('Connection successful!')
    else:
        print('Connection failed!')
    print('Status code:', response.status_code)
    print('Response:', response.json())


list_app = PythonOperator(
    task_id='list_apps',
    python_callable=list_app,
    dag=dag
)


create_db = PythonOperator(
    task_id='create_database',
    python_callable=create_db,
    dag=dag
)

list_db = PythonOperator(
    task_id='list_databases',
    python_callable=list_db,
    dag=dag
)

list_app >> create_db >> list_db
