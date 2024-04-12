from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from pathlib import Path
import os
import logging



# Default parameters for the workflow
default_args = {
    'depends_on_past': False,
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 12),
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}
with DAG(
        'daily_data_pollution_ingestion', # Name of the DAG / workflow
        default_args=default_args,
        catchup=False,
        schedule='0 5 * * *',  # Daily at 5am
) as dag:
    retrieve_daily_data = BashOperator(
        task_id='retrieve_daily_data',
        bash_command='python Scripts/daily_pollution_data_import.py',
        dag=dag,
        cwd='{{ dag_run.dag.folder }}'
    )

    retrieve_daily_data 