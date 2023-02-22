import findspark
findspark.init()
findspark.find()

from pyspark.sql import SparkSession

spark = (SparkSession.builder
                .config("conf spark.sql.extensions","com.datastax.spark.connector.CassandraSparkExtensions")
                .config("spark.cassandra.connection.host", "localhost")
                .config('spark.cassandra.connection.port', '9042')
                .config("spark.cassandra.auth.username", "cassandra")
                .config("spark.cassandra.auth.password", "cassandra")
                .appName("demo_cassandra_app").getOrCreate()
                )


spark.read \
    .format("org.apache.spark.sql.cassandra") \
    .options(table="employee", keyspace="sample_db") \
    .load().show()