from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1,
}

with DAG(
    dag_id='crypto_data_processing_mapreduce',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    start_task = DummyOperator(
        task_id='start'
    )

    fetch_and_store_task = DummyOperator(
        task_id='fetch_and_store_raw_data',
    )

    run_mapreduce_job = BashOperator(
        task_id='run_mapreduce_job',
        bash_command="""
                docker exec namenode bash -c "cd /home && \
                hadoop fs -rm -r /user/root/crypto/processed/YYYY={{ execution_date.year }}/MM={{ execution_date.strftime('%m') }}/DD={{ execution_date.strftime('%d') }} || true && \
                hadoop jar /opt/hadoop-3.2.1/share/hadoop/tools/lib/hadoop-streaming-3.2.1.jar \
                -input /user/root/crypto/YYYY={{ execution_date.year }}/MM={{ execution_date.strftime('%m') }}/DD={{ execution_date.strftime('%d') }}/crypto_historical_data.csv \
                -output /user/root/crypto/processed/YYYY={{ execution_date.year }}/MM={{ execution_date.strftime('%m') }}/DD={{ execution_date.strftime('%d') }} \
                -mapper '/usr/bin/python3 /home/mapper.py' \
                -reducer '/usr/bin/python3 /home/reducer.py' \
                -file /home/mapper.py \
                -file /home/reducer.py"
            """,
    )

    end_task = DummyOperator(
        task_id='end'
    )

    start_task >> fetch_and_store_task >> run_mapreduce_job >> end_task

