"""
Airflow DAG for the Cryptocurrency Market Analysis Pipeline

Tasks:
1. Fetch data from the CoinGecko API.
2. Store raw JSON in HDFS (organized by date).
3. Run a Hadoop MapReduce job to process the data.
4. Load the processed data into HBase.
"""

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import requests, json, subprocess

# Set default arguments
default_args = {
    'owner': 'etudiant',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def fetch_coingecko_data(**context):
    """Fetch data from the CoinGecko API."""
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': '100',
        'page': '1',
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    # Debug print: uncomment for debugging if needed:
    print("Status code:", response.status_code, "Response:", response.text)
    if response.status_code != 200:
        raise Exception("Error fetching data from CoinGecko.")
    data = response.json()
    # Push data to XCom for downstream tasks
    context['ti'].xcom_push(key='raw_data', value=data)

def store_raw_data_in_hdfs(**context):
    """Store raw JSON data in HDFS, partitioned by date."""
    data = context['ti'].xcom_pull(key='raw_data')
    json_data = json.dumps(data)
    local_file = '/tmp/coingecko_raw.json'
    with open(local_file, 'w') as f:
        f.write(json_data)
    # Use the execution date to create the partition
    execution_date = context['ds']  # Format: 'YYYY-MM-DD'
    year, month, day = execution_date.split('-')
    hdfs_dir = f"/user/etudiant/crypto/raw/YYYY={year}/MM={month}/DD={day}"
    hdfs_file_path = f"{hdfs_dir}/coingecko_raw.json"
    # Create the HDFS directory and put the file
    subprocess.run(["hdfs", "dfs", "-mkdir", "-p", hdfs_dir], check=True)
    subprocess.run(["hdfs", "dfs", "-put", "-f", local_file, hdfs_file_path], check=True)

with DAG('crypto_pipeline_dag',
         default_args=default_args,
         schedule_interval='@daily') as dag:

    fetch_data = PythonOperator(
        task_id='fetch_data',
        python_callable=fetch_coingecko_data,
        provide_context=True
    )

    store_raw_data = PythonOperator(
        task_id='store_raw_data_in_hdfs',
        python_callable=store_raw_data_in_hdfs,
        provide_context=True
    )

    run_mapreduce_job = BashOperator(
        task_id='run_mapreduce_job',
        bash_command="""
        hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
          -input /user/etudiant/crypto/raw/YYYY={{ execution_date.year }}/MM={{ execution_date.strftime('%m') }}/DD={{ execution_date.strftime('%d') }}/coingecko_raw.json \
          -output /user/etudiant/crypto/processed/YYYY={{ execution_date.year }}/MM={{ execution_date.strftime('%m') }}/DD={{ execution_date.strftime('%d') }} \
          -mapper /home/quixil/airflow/scripts/mapper.py \
          -reducer /home/quixil/airflow/scripts/reducer.py \
          -file /home/quixil/airflow/scripts/mapper.py \
          -file /home/quixil/airflow/scripts/reducer.py
        """
    )

    load_to_hbase = PythonOperator(
        task_id='load_to_hbase',
        python_callable=lambda **context: __import__('load_to_hbase').load_processed_data(context['ds']),
        provide_context=True
    )

    # Define task order
    fetch_data >> store_raw_data >> run_mapreduce_job >> load_to_hbase

