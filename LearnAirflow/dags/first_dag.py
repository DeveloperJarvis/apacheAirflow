
import os
import shutil

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator  # Updated import for Airflow 1.x
# from airflow.operators.python import PythonOperator  # Updated import for Airflow 2.x

import pandas as pd

def first_function_execute(*args, **kwargs):
    print("First function execute..")
    variable = kwargs.get("name", "user")
    string = "Hello World!!!..: {}".format(variable)
    print(string)
    return string


def second_pre_function_execute(**context):
    print("Second pre function execute..")
    context["ti"].xcom_push(
        key="mykey",
        value="pre function says hello"
        )


def second_function_execute(**context):
    instance = context.get("ti").xcom_pull(key="mykey")
    print("second_function_execute got value: {}".format(instance))

def third_function_execute():
    try:
        print("Second function execute..")
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
        python_callable=first_function_execute,
        op_kwargs={"name": "Developer Jarvis"}
    )

    second_pre_function_task = PythonOperator(
        task_id="second_pre_function_execute",
        python_callable=second_pre_function_execute,
        provide_context=True, # enable this tag you could exchange 
                                # data between this functions
        op_kwargs={"name": "Developer Jarvis"}
    )

    second_function_task = PythonOperator(
        task_id="second_function_execute",
        python_callable=second_function_execute,
        provide_context=True, # enable this tag you could exchange 
                                # data between this functions
        op_kwargs={"name": "Developer Jarvis"}
    )

    third_function_task = PythonOperator(
        task_id="third_function_execute",
        python_callable=third_function_execute
    )

second_pre_function_task >> second_function_task