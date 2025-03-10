FROM apache/airflow:2.7.0-python3.9

# Set the working directory
USER root
RUN apt-get update && apt-get install -y \
    krb5-user \
    libkrb5-dev
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install happybase
RUN pip install --no-cache-dir \
    pandas \
    yfinance \






