import yfinance as yf
import pandas as pd
import subprocess
from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


def fetch_historical_data():
    """Fetch historical cryptocurrency data using yfinance and save it to a CSV."""
    symbols = ['BTC-USD', 'ETH-USD', 'LTC-USD', 'XRP-USD', 'ADA-USD', 
               'DOT-USD', 'BNB-USD', 'SOL-USD', 'LINK-USD', 'UNI-USD', 
               'XLM-USD', 'DOGE-USD', 'XMR-USD', 'XTZ-USD']

    all_data = []

    for symbol in symbols:
        crypto = yf.Ticker(symbol)
        hist = crypto.history(period="30d")

        if not hist.empty:
            for date, row in hist.iterrows():
                all_data.append({
                    'symbol': symbol,
                    'date': date.date(),
                    'open_price': row['Open'],
                    'high_price': row['High'],
                    'low_price': row['Low'],
                    'close_price': row['Close'],
                    'volume': row['Volume']
                })

    df = pd.DataFrame(all_data)
    file_path = '/tmp/crypto_historical_data.csv'
    df.to_csv(file_path, index=False)
    return file_path


def upload_to_hdfs(**context):
    """Upload the local CSV file to HDFS with a partitioned path based on execution date."""
    local_file = '/tmp/crypto_historical_data.csv'
    execution_date = context['ds']
    year, month, day = execution_date.split('-')
    hdfs_dir = f"/user/root/crypto/YYYY={year}/MM={month}/DD={day}"
    hdfs_file_path = f"{hdfs_dir}/crypto_historical_data.csv"

    bash_command = (
        f'docker cp /tmp/crypto_historical_data.csv namenode:/tmp/crypto_historical_data.csv &&'
        f'docker exec namenode bash -c "hdfs dfs -mkdir -p {hdfs_dir} && '
        f'hdfs dfs -put -f {local_file} {hdfs_file_path}"'
    )

    result = subprocess.run(bash_command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {bash_command}\nError: {result.stderr}")


# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='fetch_crypto_data_and_upload_to_hdfs',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    start_task = DummyOperator(
        task_id='start'
    )

    fetch_data_task = PythonOperator(
        task_id='fetch_historical_data',
        python_callable=fetch_historical_data
    )

    upload_to_hdfs_task = PythonOperator(
        task_id='upload_to_hdfs',
        python_callable=upload_to_hdfs,
        provide_context=True
    )

    end_task = DummyOperator(
        task_id='end'
    )

 
    start_task >> fetch_data_task >> upload_to_hdfs_task >> end_task