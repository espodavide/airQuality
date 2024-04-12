from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.models import Variable
import logging


#getting variables 
start_date = Variable.get("start_date")
end_date = Variable.get("end_date")
print(start_date)



# Default parameters for the workflow
default_args = {
    'depends_on_past': False,
    'owner': 'airflow',
    'start_date': datetime(2024, 4, 10),
    'retries': 1,
    'retry_delay': timedelta(minutes=10)
}
logging.info("Percorso del file temporaneo di Airflow: %s", 'path_del_file_temporaneo')
with DAG(
        'batch_data_pollution_ingestion',
        default_args=default_args,
        catchup=False
) as dag:
    retrieve_batch_data = BashOperator(
        task_id='retrieve_batch_data',
        bash_command=f'python Scripts/batch_pollution_data_import.py {start_date} {end_date} ',
        dag=dag,
        cwd='{{ dag_run.dag.folder }}'
    )


    retrieve_batch_data 