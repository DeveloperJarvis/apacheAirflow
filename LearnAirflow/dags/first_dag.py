
import os
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator  # Updated import for Airflow 1.x
# from airflow.operators.python import PythonOperator  # Updated import for Airflow 2.x

import pandas as pd

def first_function_execute():
    try:
        string = "Hello World!!!.."
        print(string)

        # Define the path to the directory you want to access
        directory_path = './files'

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
            updated_df = df[df['Contact'].notnull()]
        return updated_df
    except Exception as e:
        print(f"Error reading Excel file: {e}")

# Define the DAG
with DAG(
    dag_id="first_dag",
    schedule_interval="@daily", 
    default_args={
        "owner": "airflow",
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2024, 11, 1),  # Any date or old date
    },
    catchup=False
) as dag:  # Use 'dag' as the context manager variable name
    first_function_task = PythonOperator(
        task_id="first_function_execute",
        python_callable=first_function_execute
    )