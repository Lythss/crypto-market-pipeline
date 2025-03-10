# Crypto Data Pipeline with Hadoop, Airflow, and Docker 🚀

A comprehensive pipeline for collecting, processing, and analyzing cryptocurrency data, designed to leverage Big Data and automation.

---

## 🎯 Project Objectives

This project aims to build a robust data pipeline that:

- **Collects** near real-time cryptocurrency price and volume data via the [CoinGecko API](https://www.coingecko.com/en/api) 📡.
- **Transforms** and **aggregates** data using MapReduce in Python 🔄.
- **Stores** both raw and processed data in a Hadoop-based Data Lake 🗄️.
- **Orchestrates** tasks with Apache Airflow to ensure smooth automation ⚙️.
- **Optimizes** data retrieval for fast queries using HBase 🚄.

This infrastructure is scalable and modular, capable of supporting complex analyses on large volumes of data.

---

## 🛠️ Components and Main Steps

### 1️⃣ Data Ingestion

- **Source:**  
  Daily retrieval of cryptocurrency prices and volumes using the [CoinGecko API](https://www.coingecko.com/en/api).

- **Process:**  
  An Airflow DAG fetches the data and stores it in the Data Lake.

---

### 2️⃣ Data Storage in a Data Lake

- **System:**  
  Raw data is stored in **HDFS (Hadoop Distributed File System)**.

- **Benefits:**  
  - **Scalability:** Easily handles large datasets 📈.
  - **Fault Tolerance:** Ensures data resilience 🔒.
  - **High Availability:** Supports concurrent data processing ⚡.

---

### 3️⃣ Data Transformation and Aggregation (MapReduce in Python)

- **Preprocessing:**  
  - **Data Cleaning:** Validating fields and managing missing values 🧹.
  - **Transformation:** Standardizing and normalizing the data 🔄.

- **Aggregation:**  
  Key metrics calculated include:
  - **Price Metrics:** Average, minimum, and maximum prices 💰.
  - **Volume Metrics:** Average and total volume 📊.
  - **Trend Analysis:** Variations over defined periods 📉📈.

- **Output Format:**  
  Results are generated in CSV or Parquet format for easy analysis 📑.

---

### 4️⃣ Loading into HBase

- **Optimized Querying:**  
  Processed data is loaded into **HBase** to support fast, efficient queries (e.g., searching by crypto ID and date) 🔍.

---

### 5️⃣ Orchestration with Apache Airflow

- **Task Scheduling:**  
  Automates the entire process from data ingestion to loading via Airflow DAGs ⏱️.

- **Monitoring:**  
  Real-time tracking of task executions via an intuitive web interface at [http://localhost:8080](http://localhost:8080) 🖥️.

- **Resilience:**  
  Automatic task retries and dependency management ensure robust pipeline execution 🔄.

---

## 🏗️ Architecture & Design of the Hadoop Data Lake

```mermaid
graph TD;
    A[CoinGecko API 📡] --> B[DAG for Ingestion (Airflow) ⏱️];
    B --> C[Raw Zone in HDFS 🗄️];
    C --> D[DAG for Processing (Airflow + MapReduce) 🔄];
    D --> E[Processed Zone in HDFS 📑];
    E --> F[HBase for Fast Queries 🔍];
    F --> G[Analytics/BI Dashboard 📊];
```

## Architecture Overview

- **CoinGecko API:**  
  The primary data source delivering real-time cryptocurrency data.

- **Ingestion DAG:**  
  Managed by Airflow to automate data collection and initial storage in HDFS.

- **Raw Data Zone:**  
  Maintains original data, ensuring traceability and backup for further analysis.

- **Processing DAG:**  
  Uses MapReduce jobs to clean, transform, and aggregate data, creating a structured output.

- **HBase Storage:**  
  Stores processed data for rapid querying and integration with BI tools.

- **Analytics/BI:**  
  Enables advanced visualization and analytical reporting through integrated dashboards.

---

## 🐳 Deployment with Docker & Docker Compose

### Containerization Objectives

The project is fully containerized to simplify deployment and service isolation. Each component runs in its own container, ensuring:

- **Portability:**  
  Easily deployable on any Docker-compatible environment 🌍.
- **Scalability:**  
  Seamless scaling of individual components as needed 🚀.
- **Consistency:**  
  Isolated dependencies and configurations for each service 🔒.

### Container Structure

- **Hadoop:**  
  Includes HDFS, YARN, and MapReduce services.
- **HBase:**  
  Dedicated to storing and querying processed data.
- **Apache Airflow:**  
  Manages scheduling with Scheduler, Webserver, and Worker components.
- **Python:**  
  Runs scripts for data processing and transformation.

---

## ▶️ Getting Started

### 1️⃣ Clone the Repository

```bash
git clone <REPOSITORY_URL>
cd <project_name>
```

### 2️⃣ Start the Containers

```bash
docker-compose up -d
```

3️⃣ Access the Airflow Interface

Open your browser and navigate to:
http://localhost:8080

4️⃣ Explore HBase

Use the HBase shell within the container to run queries on processed data:

```bash
docker exec -it <hbase_container_name> hbase shell
```

5️⃣ Stop the Containers

To stop all running services, execute:
```bash
docker-compose down
```

⚙️ Prerequisites & Dependencies

    Docker & Docker Compose:
    Ensure Docker is installed and that you have the necessary permissions.
    Git:
    For repository cloning and version control.
    Internet Access:
    Required for fetching data from the CoinGecko API and downloading Docker images.
    System Requirements:
    A minimum of 8 GB RAM is recommended for running Hadoop and Airflow containers efficiently.

🔍 Debugging & Monitoring

    Docker Logs:
    To view logs of a specific container, run:
```bash
    docker logs <container_name>
```
    Airflow Web UI:
    Monitor DAGs and troubleshoot errors via the Airflow dashboard.
    HBase Shell:
    Validate data and test queries interactively.

📚 Resources & Documentation

    Hadoop Documentation
    Airflow Documentation
    Docker Compose Guide
    CoinGecko API

🤝 Contributing

Contributions are welcome! If you have suggestions, improvements, or bug fixes, please create an issue or submit a pull request.
