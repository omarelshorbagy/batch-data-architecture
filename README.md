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
3. Run the following command from the root directory:   start.bat

This script will:
- Start all Docker containers (Kafka, Spark, PostgreSQL, etc.)
- Run the Kafka producer to ingest data
- Submit the Spark job to process the data
- Launch the Streamlit dashboard in a new terminal window

## How to Run Only the Dashboard

If you want to view the dashboard only (assuming the database is already populated), run the following command from the root directory:

python -m streamlit run ml_app/app.py


PostgreSQL must be running for this to work.


