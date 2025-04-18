from kafka import KafkaProducer
import pandas as pd
import json
import time

# === CONFIG ===
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'transactions'
EXCEL_FILE = 'dataset/bankdataset.xlsx'  # Path to your .xlsx file
SHEET_NAME = 0  # Or specify sheet name like 'Sheet1'

# === Kafka Setup ===
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    api_version=(2, 8, 1)  # <-- This is the fix
)


def send_excel_to_kafka():
    # Load the Excel file into a DataFrame
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

    # Fix the Timestamp column so it can be JSON serialized
    df['Date'] = df['Date'].astype(str)

    batch = []
    batch_size = 100

    for i, row in enumerate(df.to_dict(orient='records'), 1):
        batch.append(row)
        if i % batch_size == 0:
            producer.send(KAFKA_TOPIC, batch)
            print(f" Sent batch up to row {i}")
            batch = []
            time.sleep(1)

    if batch:
        producer.send(KAFKA_TOPIC, batch)
        print(f" Sent final batch of {len(batch)}")

    producer.flush()
    print(" All data sent.")


if __name__ == '__main__':
    send_excel_to_kafka()
