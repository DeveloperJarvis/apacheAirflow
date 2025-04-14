
import logging
from pathlib import Path
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from datetime import datetime

def fetch_data(**kwargs):
    """Fetch data from files in the directory and save combined CSV to temp."""
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

            logging.info(f"Data from {file.name}:
{df.head()}")
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        temp_path = "/tmp/combined_data.csv"
        combined_df.to_csv(temp_path, index=False)
        kwargs['ti'].xcom_push(key='data_path', value=temp_path)

    except Exception as e:
        logging.error("Error reading files", exc_info=True)
        raise

def approve_data(**kwargs):
    """Simulate approval of data."""
    path = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='data_path')
    df = pd.read_csv(path)
    logging.info(f"Data for approval:
{df.head()}")

    if df.empty:
        logging.warning("No data to approve.")
        return 'alert_rejection'

    decision = 'approved'  # Simulated
    return 'load_data' if decision == 'approved' else 'alert_rejection'

def load_data(**kwargs):
    """Simulate loading data into the database."""
    path = kwargs['ti'].xcom_pull(task_ids='fetch_data', key='data_path')
    df = pd.read_csv(path)
    logging.info("Loading data into the database...")
    logging.info(df.head())
    return "Data loaded successfully."

def alert_rejection():
    """Simulate sending an alert when the data is rejected."""
    logging.warning("Alert: Data has been rejected.")

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 11),
    'retries': 1,
    'email_on_failure': True,
    'email': ['alerts@example.com'],
}

with DAG(
    'approval_rejection_dag',
    default_args=default_args,
    description='A workflow with approval and rejection tasks',
    schedule_interval=None,
    catchup=False,
) as dag:

    start = DummyOperator(task_id='start')
    fetch = PythonOperator(task_id='fetch_data', python_callable=fetch_data)
    approve = PythonOperator(task_id='approve_data', python_callable=approve_data)
    load = PythonOperator(task_id='load_data', python_callable=load_data)
    alert = PythonOperator(task_id='alert_rejection', python_callable=alert_rejection)

    start >> fetch >> approve
    approve >> [load, alert]
