@echo off
echo ================================
echo  Starting Docker containers...
echo ================================
docker-compose up -d

echo.
echo  Waiting 15 seconds for services to initialize...
timeout /t 15 >nul

echo.
echo  Running Kafka producer...
python kafka\producer.py

echo.
echo  Submitting Spark job via Docker...
docker exec batch-data-architecture-spark-1 spark-submit ^
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.postgresql:postgresql:42.2.18 ^
  /opt/bitnami/spark/jobs/spark_job.py

echo.
echo  Launching ML Streamlit dashboard in a new terminal...
start cmd /k python -m streamlit run ml_app\app.py
