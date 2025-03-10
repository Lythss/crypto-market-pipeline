# Import necessary modules from Airflow:
# - DAG: To define the workflow.
# - DummyOperator: To create placeholder tasks.
# - BashOperator: To run bash commands within a task.
# - days_ago: To define the start date relative to the current time.
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Define default arguments for the DAG.
# These are used for all tasks unless overridden.
default_args = {
    'owner': 'airflow',             # Owner of the DAG.
    'depends_on_past': False,       # This task does not depend on previous runs.
    'start_date': days_ago(1),      # Set the start date to 1 day ago.
    'retries': 1,                   # Number of retries in case a task fails.
}

# Define the DAG using a context manager.
# The DAG is named 'crypto_data_processing_mapreduce', scheduled to run daily.
with DAG(
    dag_id='crypto_data_processing_mapreduce',
    default_args=default_args,
    schedule_interval='@daily',    # This DAG runs once per day.
    catchup=False,                 # Do not run past missed schedules.
) as dag:
    # Define a starting dummy task to mark the beginning of the workflow.
    start_task = DummyOperator(task_id='start')
    
    # Define a dummy task to represent fetching and storing raw data.
    # This task acts as a placeholder and can be replaced with a real task if needed.
    fetch_and_store_task = DummyOperator(task_id='fetch_and_store_raw_data')
    
    # Define a BashOperator task to run a MapReduce job using Hadoop Streaming.
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
            """
    )
    # Explanation of the Bash command above:
    # 1. Uses `docker exec` to run commands inside the 'namenode' container.
    # 2. Changes directory to /home inside the container.
    # 3. Removes any previous output directory in HDFS for the current execution date (ignoring errors with '|| true').
    # 4. Runs the Hadoop streaming job with the specified jar file:
    #    - Sets the input path to the raw data CSV (partitioned by execution date).
    #    - Sets the output path for processed data.
    #    - Specifies the mapper and reducer scripts to use.
    #    - Includes the mapper and reducer script files.
    
    # Define an ending dummy task to mark the end of the workflow.
    end_task = DummyOperator(task_id='end')
    
    # Set the execution order of the tasks:
    # The workflow flows from start_task -> fetch_and_store_task -> run_mapreduce_job -> end_task.
    start_task >> fetch_and_store_task >> run_mapreduce_job >> end_task
