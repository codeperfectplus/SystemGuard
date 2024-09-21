#!/bin/bash

# Define variables
INFLUXDB_VERSION="latest"
CONTAINER_NAME="influxdb"
NETWORK_NAME="influx_network"
DATA_DIR="./influxdb_data"
INFLUXDB_USER="admin"                # Change this to your desired username
INFLUXDB_PASSWORD="admin_password"         # Change this to your desired password
INFLUXDB_ORG="systemguard"                # Change this to your desired organization name
INFLUXDB_BUCKET="system_metrics"     # Change this to your desired initial bucket (database) name
# demo influxdb token | change this to your own token
INFLUXDB_TOKEN=""

# Export the INFLUXDB_TOKEN to be used later in your app
export "INFLUXDB_TOKEN"=$INFLUXDB_TOKEN

# Create a data directory for InfluxDB
rm -rf $DATA_DIR
mkdir -p $DATA_DIR

# Stop and remove existing InfluxDB container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing InfluxDB container..."
    docker stop $CONTAINER_NAME
    echo "Removing existing InfluxDB container..."
    docker rm -f $CONTAINER_NAME
fi

# Kill any process using port 8086
if sudo lsof -i :8086; then
    echo "Killing process using port 8086..."
    sudo fuser -k 8086/tcp
fi

# Create a Docker network
echo "Creating Docker network..."
docker network create $NETWORK_NAME || true  # Avoid error if the network already exists

# Pull the InfluxDB Docker image
echo "Pulling InfluxDB Docker image..."
docker pull influxdb:$INFLUXDB_VERSION

# Run the InfluxDB container with authentication and initial setup to skip onboarding
echo "Running InfluxDB container..."
docker run -d \
  --name $CONTAINER_NAME \
  --network $NETWORK_NAME \
  --restart=always \
  -p 8086:8086 \
  -v $PWD/$DATA_DIR:/var/lib/influxdb2 \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=$INFLUXDB_USER \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=$INFLUXDB_PASSWORD \
  -e DOCKER_INFLUXDB_INIT_ORG=$INFLUXDB_ORG \
  -e DOCKER_INFLUXDB_INIT_BUCKET=$INFLUXDB_BUCKET \
  -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=$INFLUXDB_TOKEN \
  influxdb:$INFLUXDB_VERSION


# Output completion message
echo "InfluxDB setup completed! Access it at http://localhost:8086 with your credentials."