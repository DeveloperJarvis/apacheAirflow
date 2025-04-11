from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime
import pandas as pd
import psycopg2
import os

# # Function to fetch data from Excel
# def fetch_data(**kwargs):
#     # Read data from the Excel file
#     data = pd.read_excel('./files/Data.xlsx')
#     # Store the data in XCom for later use
#     kwargs['ti'].xcom_push(key='data', value=data.to_dict(orient='records'))
def fetch_data(**kwargs):
    # Load data from Excel file
    try:
        print("fetch_data execute..")
        # Define the path to the directory you want to access
        # directory_path = config.directory_path
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
            # updated_df = df[df['Contact'].notnull()]
            # Store the data in XCom for later use
        kwargs['ti'].xcom_push(key='data', value=df.to_dict(orient='records'))
    except Exception as e:
        print(f"Error reading Excel file: {e}")

# Function to process and load data into PostgreSQL
def load_data_to_postgres(**kwargs):
    # Retrieve the data from XCom
    data = kwargs['ti'].xcom_pull(key='data', task_ids='fetch_data')
    
    # Connect to PostgreSQL
    conn = psycopg2.connect("""
                            dbname='your_db' 
                            user='your_user' 
                            password='your_password' 
                            host='localhost'
                            """)
    cursor = conn.cursor()
    
    # Assuming data is a list of dictionaries
    for row in data:
        cursor.execute("INSERT INTO analytics_data (column1, column2) VALUES (%s, %s)", 
                       (row['column1'], row['column2']
                       ))
    
    conn.commit()
    cursor.close()
    conn.close()

# Define the DAG
dag = DAG(
    'approval_workflow',
    default_args={
        'owner': 'airflow',
        'start_date': datetime(2025, 4, 10),
        'retries': 1,
    },
    schedule_interval=None,
)

# Task for fetching data
fetch_data_task = PythonOperator(
    task_id='fetch_data',
    python_callable=fetch_data,
    provide_context=True,  # Allows access to context variables
    dag=dag,
)

# Task for sending approval request
request_approval = EmailOperator(
    task_id='request_approval',
    to='analyst@local.test',
    subject='Approval Required',
    html_content='Please review the data for approval.',
    dag=dag,
)

# Task for loading data if approved
load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    provide_context=True,  # Allows access to context variables
    dag=dag,
)

# Define task dependencies
fetch_data_task >> request_approval >> load_data_task