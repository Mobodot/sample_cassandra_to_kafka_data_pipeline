
sudo docker run -i \
-p 7000:7000 \
-p 9042:9042 \
-e CASSANDRA_CLUSTER_NAME=cassandra-cluster \
-e CASSANDRA_USERNAME=cassandra \
-e CASSANDRA_PASSWORD_SEEDER=yes \
-e CASSANDRA_PASSWORD=cassandra \
-v $PROJECT_DIR/cassandra_data:/bitnami \
--name cassandraDB \
a6b7d365e47d
