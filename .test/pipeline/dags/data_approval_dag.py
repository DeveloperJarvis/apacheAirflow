from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.models import Variable
from datetime import datetime
import pandas as pd
import psycopg2
import os

from ..config import config

def fetch_data():
    # Load data from Excel file
    try:
        print("fetch_data execute..")
        # Define the path to the directory you want to access
        directory_path = config.directory_path

        # List all files in the directory
        files = os.listdir(directory_path)
        print("Files in directory:", files)

        for file in files:
            print(file)
            full_file_path = os.path.join(directory_path, file)
            if file.endswith(".csv"):
                df = pd.read_csv(full_file_path, engine='python')
            elif file.endswith(".xlsx"):
                df = pd.read_excel(full_file_path, engine='openpyxl') # For .xlsx files
            elif file.endswith(".xls"):
                df = pd.read_excel(directory_path, engine='xlrd')  # For .xls files
            print(df)
            # updated_df = df[df['Contact'].notnull()]
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")

def approve_data(**kwargs):
    # Logic to approve data
    df = kwargs['ti'].xcom_pull(task_ids='fetch_data')
    # Here you can implement your approval logic
    # For example, you can check if the data meets certain criteria
    if df['status'].iloc[0] == 'approved':
        return 'load_data'
    else:
        return 'alert_rejection'

def load_data(**kwargs):
    df = kwargs['ti'].xcom_pull(task_ids='fetch_data')
    # Connect to PostgreSQL and load data
    conn = psycopg2.connect(f"""
                                dbname={config.sql_dbname}
                                user={config.sql_user} 
                                host={config.sql_host}
                                password={config.sql_password}
                                """)
    cursor = conn.cursor()
    for index, row in df.iterrows():
        cursor.execute("""
            INSERT INTO your_table (column1, column2) "
            "VALUES (%s, %s)""", (row['column1'], row['column2']))
    conn.commit()
    cursor.close()
    conn.close()

def alert_rejection():
    # Logic to send alert
    print("Data has been rejected.")

with DAG('data_approval_dag', start_date=datetime(2023, 10, 1), schedule_interval=None) as dag:
    start = DummyOperator(task_id='start')
    fetch = PythonOperator(task_id='fetch_data', python_callable=fetch_data)
    approve = PythonOperator(task_id='approve_data', python_callable=approve_data, provide_context=True)
    load = PythonOperator(task_id='load_data', python_callable=load_data, provide_context=True)
    alert = PythonOperator(task_id='alert_rejection', python_callable=alert_rejection)

    start >> fetch >> approve
    approve >> load
    approve >> alert    