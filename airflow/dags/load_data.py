from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import happybase
import subprocess
import os
from airflow.exceptions import AirflowException

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

def load_processed_data(ds):
    year, month, day = ds.split('-')
    hdfs_dir = f"/user/root/crypto/processed/YYYY={year}/MM={month}/DD={day}/"
    local_file = "/tmp/crypto_agg.csv"

    try:
        subprocess.run(
            ["docker", "exec", "namenode", "hdfs", "dfs", "-get", f"{hdfs_dir}part-00000", "/tmp/crypto_agg.csv"],
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["docker", "cp", "namenode:/tmp/crypto_agg.csv", local_file],
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ["docker", "exec", "namenode", "rm", "-f", "/tmp/crypto_agg.csv"],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        raise AirflowException(f"Failed to fetch HDFS file: {e.stderr}")

    if not os.path.exists(local_file):
        raise AirflowException(f"HDFS file not found at {local_file} after fetch")

    try:
        connection = happybase.Connection('hbase-master', port=9090)
        if 'crypto_prices' not in connection.tables():
            print("Creating table 'crypto_prices'")
            connection.create_table(
                'crypto_prices',
                {'stats': dict(max_versions=3)}  # Removed blockcache
            )
        table = connection.table('crypto_prices')

        with table.batch() as batch:
            with open(local_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        coin_id, agg_str = line.split("\t")
                        min_p, max_p, avg_p, std_p, vol_sum, c = agg_str.split(",")
                    except ValueError:
                        print(f"Skipping malformed line: {line}")
                        continue

                    row_key = f"{coin_id}_{ds}"
                    batch.put(row_key, {
                        b'stats:price_min': min_p.encode(),
                        b'stats:price_max': max_p.encode(),
                        b'stats:price_avg': avg_p.encode(),
                        b'stats:price_std_dev': std_p.encode(),
                        b'stats:volume_sum': vol_sum.encode(),
                        b'stats:count': c.encode()
                    })

    except Exception as e:
        raise AirflowException(f"Failed to load data into HBase: {str(e)}")
    finally:
        if 'connection' in locals():
            connection.close()
        if os.path.exists(local_file):
            os.remove(local_file)

with DAG(
    dag_id='load_to_hbase',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:
    load_into_hbase = PythonOperator(
        task_id='load_into_hbase',
        python_callable=load_processed_data,
        op_kwargs={'ds': '{{ ds }}'},
    )

    load_into_hbase