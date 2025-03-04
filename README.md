# 🚀 Crypto Market Pipeline

A Big Data pipeline for cryptocurrency market analysis using the [CoinGecko API](https://www.coingecko.com/en/api) for data ingestion, **HDFS** for raw storage, **Python MapReduce** for data transformation, **HBase** for structured storage, and **Apache Airflow** for orchestration.

---

## ✨ Features

- **Daily Ingestion** of crypto data from CoinGecko (top 100 by market cap).
- **Data Lake (HDFS)** partitioned by date for raw storage.
- **MapReduce** (Python scripts) for cleaning and aggregating:
  - Min, max, average, standard deviation of prices
  - Volume sums
- **HBase** loading for fast queries by date and coin ID.
- **Orchestration** with Airflow to schedule and monitor the entire pipeline.

---

## 🏗️ Architecture Overview

```plaintext
            ┌──────────────────────────┐
            │  CoinGecko API (Daily)  │
            └───────────┬─────────────┘
                        │
         ┌──────────────▼───────────────┐
         │ Airflow DAG: Ingestion       │
         │ (Fetch API + Store in HDFS)  │
         └──────────────┬───────────────┘
                        │
             HDFS (Raw Data Partitioned by Date)
                        │
         ┌──────────────▼───────────────┐
         │ Airflow DAG: Processing      │
         │ (MapReduce in Python)        │
         └──────────────┬───────────────┘
                        │
           HDFS (Processed / Curated Data)
                        │
         ┌──────────────▼───────────────┐
         │           HBase              │
         │ (for fast queries/analysis)  │
         └──────────────┬───────────────┘
                        │
                     Analytics / BI

# Crypto Market Pipeline

## 📋 Prerequisites
- Python 3.8+
- Apache Hadoop (3.x or later)
- Apache HBase (2.x or later)
- Apache Airflow (2.x or later)
- HappyBase library (for HBase in Python):

```bash
pip install happybase
```

- Requests library (for CoinGecko API):
```bash
pip install requests
```

## 🏁 Getting Started

### Clone the Repository
```bash
git clone https://github.com/Lythss/crypto-market-pipeline.git
cd crypto-market-pipeline
```

### Set Up a Python Virtual Environment (Optional)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Airflow
- Set AIRFLOW_HOME (e.g., export AIRFLOW_HOME=~/airflow).
- Place the DAG file (crypto_pipeline_dag.py) in your $AIRFLOW_HOME/dags directory or update airflow.cfg to point to the folder where the DAG resides.

### Start HDFS and HBase
```bash
start-dfs.sh
start-hbase.sh
```

### Create the HBase Table
```bash
echo "create 'crypto_prices', 'stats'" | hbase shell
```

### Start Airflow
```bash
airflow scheduler &
airflow webserver --port 8080 &
```

## 🌀 Usage

### Trigger the Pipeline
- Go to Airflow UI at http://localhost:8080.
- Locate the crypto_pipeline_dag and click "Trigger DAG."

### Monitor Tasks
Check logs for each task:
- fetch_data → retrieves data from CoinGecko
- store_raw_data_in_hdfs → writes JSON to HDFS
- run_mapreduce_job → processes data with mapper & reducer
- load_to_hbase → writes aggregated metrics to HBase

### Check HDFS
```bash
hdfs dfs -ls /user/<your_username>/crypto/raw/
hdfs dfs -ls /user/<your_username>/crypto/processed/
```

### Check HBase
```bash
hbase shell
scan 'crypto_prices', {LIMIT => 5}
```

## 🏷️ Directory Structure
```bash
crypto-market-pipeline/
├── dags/
│   └── crypto_pipeline_dag.py   # Airflow DAG
├── script/
│   ├── mapper.py               # MapReduce mapper
│   └── reducer.py              # MapReduce reducer
├── loader/
│   └── load_to_hbase.py        # Script to load data into HBase
├── docs/
│   └── metadata.md             # (Optional) Data definitions/governance
├── LICENSE
├── README.md
└── requirements.txt            # (Optional) Python dependencies
```

## 🔧 Troubleshooting
- HDFS Connection Refused: Ensure NameNode is running (start-dfs.sh) and check with jps.
- Missing mapper/reducer: Confirm the absolute paths in your DAG's run_mapreduce_job match the actual script locations.
- HBase Load Fails: Check that HBase is running and that crypto_prices table exists.
- Airflow Not Finding the DAG: Make sure your DAG file is in the dags/ folder recognized by Airflow (airflow.cfg -> dags_folder).

## 🤝 Contributing
Feel free to submit pull requests or open issues if you have suggestions or find bugs.
1. Fork this repo
2. Create a new branch
3. Make your changes
4. Submit a pull request

## 📄 License
This project is licensed under the Apache 2.0 License.

## 🎉 Acknowledgments
- CoinGecko for the free cryptocurrency market data API
- Apache Hadoop & Apache HBase for scalable storage
- Apache Airflow for orchestration
