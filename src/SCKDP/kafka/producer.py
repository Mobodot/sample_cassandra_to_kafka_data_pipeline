from SCKDP.logger import logger

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.functions import *


KEYSPACE = "sample_db"
TABLE_NAME = "employee"

KAFKA_TOPIC = "employee"
KAFKA_BOOTSTRAP_SERVER = "localhost:90922"


spark = (SparkSession.builder
            .config("spark.cassandra.connection.host", "localhost")
            .config('spark.cassandra.connection.port', '9042')
            .config("spark.cassandra.auth.username", "cassandra")
            .config("spark.cassandra.auth.password", "cassandra")
            .appName("demo_cassandra_app").getOrCreate()
            )


def createDataFrameFromCassandraTable(spark: spark, 
                                      keyspace: str,
                                      table: str) -> DataFrame:
    try:
        # read data from cassandra to spark
        df = spark.read \
                .format("org.apache.spark.sql.cassandra") \
                .options(table="employee", keyspace="sample_db") \
                .load()
        
        return df
    except Exception as e:
        logger.error(f"Unable to read cassandra data: {e}")


def sendDataToKafkaTopic(kafkaBootStrapServer: str,
                         topicName: str,
                         dataframe: DataFrame) -> None:
    
    try:
        logger.info(f"Started writing data to kafka topic *{topicName}* and server *{kafkaBootStrapServer}*")
        dataFrame = \
            dataframe.select(col("emp_id").cast(StringType()).alias("key"), 
                            to_json(struct("emp_id","emp_name","city","state")).alias("value"))
            
        dataFrame.show(2, truncate=False)
        (dataFrame.write
        .format("kafka")
        .option("kafka.bootstrap.servers", kafkaBootStrapServer)
        .option("failOnDataLoss", "false")
        .option("topic", topicName)
        .save())
        
        logger.info(f"Data has been written to kafka topic *{topicName}*")
    except Exception as e:
        logger.error(e)
        


if __name__ == "__main__":
    logger.info("Starting producer spark app ...")
    logger.info("Reading table *{TABLE_NAME}* from cassandra to spark ...")
    df = createDataFrameFromCassandraTable(spark, KEYSPACE, TABLE_NAME) 
    
    df.printSchema()
    nrows = df.count()
    columns = df.columns
    
    logger.info(f"Table *{TABLE_NAME}* has columns: [{columns}]")
    logger.info(f"{nrows}rows found in table: *{KEYSPACE}.{TABLE_NAME}*")
    
    if nrows == 0:
        logger.warn("No data found hence data will not be written to kafka topic")
    else:
        logger.info(f"Sending {nrows}records to kafka topic: *{KAFKA_TOPIC}*")
        sendDataToKafkaTopic(KAFKA_BOOTSTRAP_SERVER,
                             KAFKA_TOPIC,
                             df)