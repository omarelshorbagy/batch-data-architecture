# Batch Data Architecture — ML-Ready Data Pipeline

This project implements a batch-processing data architecture for transforming and preparing data for machine learning. It is developed using VS Code and runs entirely on Docker containers for portability and consistency.

The system includes data ingestion, processing, storage, and a dashboard to inspect the prepared dataset.

## Architecture Overview

- Kafka and Zookeeper handle incoming raw data messages.
- A Python script acts as a Kafka producer, reading data from an Excel file and sending it to Kafka.
- Apache Spark reads the Kafka stream, cleans and aggregates the data, and stores the result in PostgreSQL.
- A Streamlit dashboard is used to display the ML-ready data for analysis and inspection.
- MinIO is included for optional object storage, as described in the original system design.

## How to Run the Full Pipeline

To run the full system (including data ingestion, processing, and dashboard):

1. Make sure Docker Desktop and Python 3 are installed on your machine.
2. Open the project folder in VS Code.
3. Run the following command from the root directory:

start.bat


This script will:
- Start all Docker containers (Kafka, Spark, PostgreSQL, etc.)
- Run the Kafka producer to ingest data
- Submit the Spark job to process the data
- Launch the Streamlit dashboard in a new terminal window

## Running Services Independently

Each component in the pipeline is loosely coupled and can be run separately.

### 1. Run Only the Kafka Producer
This will send raw data to the Kafka topic:

python kafka\producer.py


Kafka and Zookeeper must be running via Docker.

### 2. Run the Spark Job Manually (Windows - outside Docker)
Ensure you are using Java 11 locally before running the Spark job:
set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.27.6-hotspot set PATH=%JAVA_HOME%\bin;%PATH% python spark\spark_job.py


Make sure Kafka and PostgreSQL containers are running in the background.

## Local PySpark Execution in VS Code
If you prefer to run `spark_job.py` locally from within VS Code (instead of Docker), you must ensure the correct Java environment is set. Spark is not compatible with Java 17 or above when used with PySpark on Windows.
you can type in the following command in the VS code terminal:

set JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.27.6-hotspot (depends on the path of the jdk installed)

set PATH=%JAVA_HOME%\bin;%PATH%

python spark\spark_job.py



### 3. Run Only the ML Dashboard
This will open the Streamlit dashboard in your browser:

python -m streamlit run ml_app\app.py

PostgreSQL must be running to fetch the ML-ready data.



