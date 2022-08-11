
import requests

from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

from airflow.providers.apache.zeppelin.operators.zeppelin_operator import ZeppelinOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2022, 6, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

ZEP_URL = "http://host.docker.internal:8890/api/notebook/job"
NOTE_ID = "2H87GW1C4"


def invoke_zep():
    res = requests.post(f"{ZEP_URL}/{NOTE_ID}", verify=False)
    print(res.json())


with DAG('dev_rest_zepp',
         max_active_runs=1,
         schedule_interval='0 0 * * *',
         default_args=default_args
         ) as dag:

    start = DummyOperator(
        task_id="start"
    )

    spark_proc = PythonOperator(
        task_id='spark_proc',
        python_callable=invoke_zep,
        retries=1
    )

    end = DummyOperator(
        task_id="end"
    )

    start >> spark_proc >> end
