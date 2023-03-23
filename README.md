# SAMPLE_CASSANDRA_TO_KAFKA_DATA_PIPELINE

This project demonstrates how to setup a development environment locally to create a data pipleline from ***cassandra*** through ***kafka*** then finally to ***hdfs*** or your local filesytem.

## Project Architecture
![system_architecture](images/cassandra_project_diagram(5).png)


## Steps to setup the project

To start the setup

1. **Create** and **activate** your virtual environment.
   
2. Run pip install requirements.txt

3. ```docker compose up -d```

4. Install ***Cassandra Workbench*** extension in vscode to work with cassandra db.

**NB**: Follow the setup process on vscode to get it started.

5. Load the data into cassandra by copying the script in CQL_SCRIPT.cql in the project home folder.
e.g:

Create a keyspace with name "sample_db"

```
CREATE KEYSPACE sample_db
	WITH REPLICATION = {
		'class': 'org.apache.cassandra.locator.SimpleStrategy',
		'replication_factor': '3'
	}
	AND DURABLE_WRITES = true;
```

Create a table employee

```
 CREATE TABLE sample_db.employee(
     EMP_ID INT,
     EMP_NAME text,
     CITY text,
     STATE text,
     primary key (EMP_ID)
 );
```

6. Insert records into the Employee table refer to CQL_SCRIPT.cql

Once above steps is completed execute the command below

To Launch producer script

```
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0 \
src/SCKDP/kafka/producer.py 
```

To launch consumer script

```
spark-submit \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1 \
src/SCKDP/kafka/consumer.py 
```

To stop the setup

```docker compose down```
