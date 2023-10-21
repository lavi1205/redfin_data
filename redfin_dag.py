import requests
import pandas as pd
import os
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# Define your default_args for the DAG
default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 10, 20),
    'retries': 10,
    'depends_on_past': False,
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

url = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/us_national_market_tracker.tsv000.gz"

def check_api_status(**kwargs):
    url = kwargs['url']
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx and 5xx)
        print(f'API CHECKING SUCCESS. CODE RETURN {response.status_code}')
    except Exception as e:
        print(f'API CHECKING FAIL\nERROR DISPLAY: {e}')

def extract_data(**kwargs):
    url = kwargs['url']
    current_time = datetime.now().strftime('%Y%m%d%H%M%S') 
    file_name = 'redfin_raw_data_' + current_time + '.csv' 
    df = pd.read_csv(url, compression='gzip', sep='\t')
    df.to_csv(file_name, index=False)
    output_data = [file_name, current_time]
    return output_data

def transform_data(**kwargs):
    ti = kwargs['ti']
    file_name = ti.xcom_pull(task_ids='task_extract_redfin_data')[0]
    current_time = ti.xcom_pull(task_ids='task_extract_redfin_data')[1]
    df = pd.read_csv(file_name)
    df.dropna(inplace=True)  # Remove rows with missing values
    df['period_begin'] = pd.to_datetime(df['period_begin'])
    df['period_end'] = pd.to_datetime(df['period_end'])

    df["period_begin_in_years"] = df['period_begin'].dt.year
    df["period_end_in_years"] = df['period_end'].dt.year

    df["period_begin_in_months"] = df['period_begin'].dt.month
    df["period_end_in_months"] = df['period_end'].dt.month

    month_dict = {
        "period_begin_in_months": {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec",
        },
        "period_end_in_months": {
            1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
        }
    }
    df_after_modify = df.replace(month_dict)
    file_name = 'redfin_data_after_process_' + current_time + '.csv'
    df_after_modify.to_csv(file_name, index=False)
    return file_name

def upload_to_s3(file_name, bucket, object_name=None):
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    s3_client = boto3.client('s3', aws_access_key_id="",
                            aws_secret_access_key="", region_name="ap-southeast-1")

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        print(f'UPLOAD TO S3 SUCCESS. S3 BUCKET: {bucket}')
    except ClientError as e:
        print(f"UPLOAD TO S3 FAILED. S3 BUCKET: {bucket}\nERROR RETURN {e}")

with DAG('redfin_analytics_dag',
        default_args=default_args,
        # schedule_interval = '@weekly',
        catchup=False) as dag:

    start = DummyOperator(
        task_id='START'
    )

    check_api_status = PythonOperator(
        task_id='check_api_status',
        python_callable=check_api_status,
        op_kwargs={'url': url}
    )

    extract_redfin_data = PythonOperator(
        task_id='task_extract_redfin_data',
        python_callable=extract_data,
        provide_context=True,
        op_kwargs={'url': url}
    )

    upload_to_s3_raw = PythonOperator(
        task_id='upload_to_S3_raw_bucket',
        python_callable=upload_to_s3,
        provide_context = True,
        op_kwargs={'file_name': "{{ task_instance.xcom_pull(task_ids='task_extract_redfin_data')[0]}}",
                   'bucket': 'raw-bucket-123'}
    )

    transform_data_task = PythonOperator(
        task_id='task_transform_redfin_data',
        python_callable=transform_data,
        provide_context=True
    )

    upload_to_s3_result = PythonOperator(
        task_id='upload_to_s3_final_data_bucket',
        python_callable=upload_to_s3,
        op_kwargs={'file_name': "{{ task_instance.xcom_pull(task_ids='task_transform_redfin_data') }}",
                   'bucket': 'final-bucket-123'}
    )

    end = DummyOperator(
        task_id='END'
    )

    start >> check_api_status >> extract_redfin_data >> upload_to_s3_raw >> transform_data_task >> upload_to_s3_result >> end
