from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, schema_of_json, explode

print(" Starting Spark Kafka-to-Postgres Batch Job...")

# === Spark Session ===
spark = SparkSession.builder \
    .appName("KafkaToPostgresProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.postgresql:postgresql:42.2.18") \
    .getOrCreate()

print(" Spark session started.")

# === Config ===
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC = "transactions"
PG_URL = "jdbc:postgresql://localhost:5432/ml_data"
PG_PROPERTIES = {
    "user": "user",
    "password": "password",
    "driver": "org.postgresql.Driver"
}

# === Step 1: Read from Kafka ===
df = spark.read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS) \
    .option("subscribe", TOPIC) \
    .option("startingOffsets", "earliest") \
    .option("endingOffsets", "latest") \
    .load()

print(f" Read {df.count()} Kafka records")

# === Step 2: Convert Kafka value to JSON string column ===
df = df.selectExpr("CAST(value AS STRING) as json")

# === Step 3: Infer schema from one sample message ===
sample_json = df.select("json").first()[0]
schema = schema_of_json(sample_json)

# === Step 4: Parse JSON array and explode into individual rows ===
parsed_df = df.withColumn("json_array", from_json(col("json"), schema))
structured_df = parsed_df.withColumn("data", explode(col("json_array"))).select("data.*")

# === Step 5: Limit & clean data ===
structured_df = structured_df.limit(500)
structured_df = structured_df.dropna()

print(f" Cleaned DataFrame — Remaining rows: {structured_df.count()}")

# === Step 6: Write to PostgreSQL ===
structured_df.write \
    .jdbc(url=PG_URL, table="ml_ready_data", mode="append", properties=PG_PROPERTIES)

print(" Spark job finished. Data written to PostgreSQL.")
spark.stop()
