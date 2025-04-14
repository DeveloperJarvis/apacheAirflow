
import logging
from pathlib import Path
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from datetime import datetime

def fetch_data(**kwargs):
    """Fetch and store combined data from a directory."""
    try:
        directory_path = Variable.get("data_file_path", default_var="./files")
        files = list(Path(directory_path).glob("*"))

        combined_df = pd.DataFrame()

        for file in files:
            if file.suffix == ".csv":
                df = pd.read_csv(file, engine='python')
            elif file.suffix == ".xlsx":
                df = pd.read_excel(file, engine='openpyxl')
            elif file.suffix == ".xls":
                df = pd.read_excel(file, engine='xlrd')
            else:
                continue
            logging.info(f"Fetched data from {file.name}")
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        temp_path = "/tmp/fetched_combined_data.csv"
        combined_df.to_csv(temp_path, index=False)
        kwargs['ti'].xcom_push(key='data_path', value=temp_path)

    except Exception as e:
        logging.error("Error reading files", exc_info=True)
        raise

def wait_for_approval(**kwargs):
    """Simulate waiting for approval from external input."""
    ti = kwargs['ti']
    approval_status = ti.xcom_pull(task_ids='approval_input_task', key='approval_status')

    if approval_status == 'approved':
        logging.info("Approval received. Proceeding with the task.")
        return 'approved_task'
    elif approval_status == 'rejected':
        logging.info("Rejection received. Stopping the task.")
        return 'rejected_task'
    else:
        logging.info("Waiting for approval...")
        return 'waiting_for_approval'

def process_data(**kwargs):
    path = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='data_path')
    df = pd.read_csv(path)
    logging.info("Processing approved data...")
    logging.info(df.head())

def send_alert(**kwargs):
    logging.warning("Data was rejected. Sending alert...")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 11),
    'retries': 1,
    'email_on_failure': True,
    'email': ['alerts@example.com'],
}

with DAG(
    'approval_rejection_v2',
    default_args=default_args,
    description='Second version of approval/rejection workflow',
    schedule_interval=None,
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start')

    fetch = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_data
    )

    approval_input_task = PythonOperator(
        task_id='approval_input_task',
        python_callable=wait_for_approval
    )

    approved_task = PythonOperator(
        task_id='approved_task',
        python_callable=process_data
    )

    rejected_task = PythonOperator(
        task_id='rejected_task',
        python_callable=send_alert
    )

    start >> fetch >> approval_input_task >> [approved_task, rejected_task]
