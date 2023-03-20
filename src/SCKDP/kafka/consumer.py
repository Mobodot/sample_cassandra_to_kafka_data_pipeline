import os
from SCKDP.logger import logger

from pyspark.sql.types import *
from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from pyspark.sql import SparkSession


KEYSPACE = "sample_db"
TABLE_NAME = "employee"

KAFKA_BOOTSTRAP_SERVER = "localhost:9092" 
PROCESSING_INTERVAL = "5 seconds"
KAFKA_TOPIC = "employee"

spark = (SparkSession.builder
            .appName("demo_cassandra_app").getOrCreate()
            )


schema = StructType([
    StructField("emp_id", IntegerType(), True),
    StructField("emp_name", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True)
])

dataSink = os.path.join("employee_data")


def processEachInterval(df: DataFrame, epoch_id):
    try:
        print(df.show(2))
        df = (df.withColumn("value",
                            from_json(decode("value", charset="UTF-8"), schema=schema)
                            .alias("value"))
                            .select("value.*")
            )
        print("--- Df after transformation----: ")
        if df.count() > 0:
            df.show(truncate=False)
            df.write.mode("append").parquet(dataSink)
    except Exception as e:
        logger.error(e)


{'bootstrap_server': {KAFKA_BOOTSTRAP_SERVER}, 'kafka_topic': {KAFKA_TOPIC}, 'starting_offset': 'earliest'}
if __name__ == "__main__":
    logger.info("Starting consumer spark app ...")
    logger.info(f"Loading kafka config: ['bootstrap_server': {KAFKA_BOOTSTRAP_SERVER}, 'kafka_topic': {KAFKA_TOPIC}, 'starting_offset': 'earliest']")
    logger.info(F"Reading Stream from kafka topic *{KAFKA_TOPIC}*")
    df = (spark
        .readStream
        .format("kafka")
        .option("kafka.bootstrap.servers",KAFKA_BOOTSTRAP_SERVER)
        .option("subscribe", KAFKA_TOPIC)
        .option("startingOffsets","earliest")
        .load()
        )

    print("printing df schema: ---->--->")
    df.printSchema()
    
    logger.info(f"writing stream to {dataSink} ...")
    query = (df.writeStream
             .trigger(processingTime=PROCESSING_INTERVAL)
             .foreachBatch(processEachInterval)
             .start()
            )
    

    query.awaitTermination()