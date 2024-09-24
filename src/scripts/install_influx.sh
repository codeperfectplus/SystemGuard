#!/bin/bash

# how to run the script | why not with the bash command
# source install_influx.sh
# as running with source update the environment variables in the current shell

# Function to get the username of the current user or logname
get_user_name() {
    if [ "$(whoami)" = "root" ]; then
        LOGNAME_USER=$(logname 2>/dev/null)
        if [ $? -ne 0 ]; then
            USER_NAME=$(grep '/home' /etc/passwd | cut -d: -f1 | tail -n 1)
        else
            USER_NAME=$LOGNAME_USER
        fi
    else
        USER_NAME=$(whoami)
    fi
    echo "$USER_NAME"
}

# Variables
INFLUXDB_VERSION="latest"
CONTAINER_NAME="influxdb"
NETWORK_NAME="influx_network"
DATA_DIR="./influxdb_data"
INFLUXDB_USER="admin"                # Desired username
INFLUXDB_PASSWORD="password"            # Desired password
INFLUXDB_ORG="systemguard"           # Organization name
INFLUXDB_BUCKET="system_metrics"     # Initial bucket name
USER_NAME=$(get_user_name)
INFLUXDB_TOKEN=$(openssl rand -base64 48)
BAHRC_FILE="/home/$USER_NAME/.bashrc"
DATABASE_DIR="/home/$USER_NAME/.database/$DATA_DIR"

# Check if INFLUXDB_TOKEN is already set in .bashrc, and update if necessary
if grep -q "export INFLUXDB_TOKEN=" "$BAHRC_FILE"; then
    sed -i "s|export INFLUXDB_TOKEN=.*|export INFLUXDB_TOKEN=$INFLUXDB_TOKEN|" "$BAHRC_FILE"
else
    echo "export INFLUXDB_TOKEN=$INFLUXDB_TOKEN" >> "$BAHRC_FILE"
fi

# Apply changes to the current session by sourcing .bashrc
source "$BAHRC_FILE"

# Verify if the token was applied to the environment
if [ -z "$INFLUXDB_TOKEN" ]; then
    echo "Failed to export INFLUXDB_TOKEN"
    exit 1
else
    echo "INFLUXDB_TOKEN successfully set."
fi

# Remove and recreate the data directory for InfluxDB
rm -rf "$DATABASE_DIR"
if ! sudo -u "$USER_NAME" mkdir -p "$DATABASE_DIR"; then
    echo "Failed to create data directory: $DATABASE_DIR"
    exit 1
fi

# Stop and remove existing InfluxDB container if it exists
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "Stopping existing InfluxDB container..."
    docker stop $CONTAINER_NAME || { echo "Failed to stop container"; exit 1; }

    echo "Removing existing InfluxDB container..."
    docker rm -f $CONTAINER_NAME || { echo "Failed to remove container"; exit 1; }
fi

# Kill any process using port 8086
if sudo lsof -i :8086; then
    echo "Killing process using port 8086..."
    sudo fuser -k 8086/tcp || { echo "Failed to kill process on port 8086"; exit 1; }
fi

# Create a Docker network if it doesn't exist
if ! docker network inspect $NETWORK_NAME >/dev/null 2>&1; then
    echo "Creating Docker network..."
    docker network create $NETWORK_NAME || { echo "Failed to create network"; exit 1; }
fi

# Pull the InfluxDB Docker image
echo "Pulling InfluxDB Docker image..."
if ! docker pull influxdb:$INFLUXDB_VERSION; then
    echo "Failed to pull InfluxDB image"
    exit 1
fi

# Run the InfluxDB container with setup options
echo "Running InfluxDB container..."
docker run -d \
  --name $CONTAINER_NAME \
  --network $NETWORK_NAME \
  --restart=always \
  -p 8086:8086 \
  -v "$DATABASE_DIR:/var/lib/influxdb2" \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=$INFLUXDB_USER \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=$INFLUXDB_PASSWORD \
  -e DOCKER_INFLUXDB_INIT_ORG=$INFLUXDB_ORG \
  -e DOCKER_INFLUXDB_INIT_BUCKET=$INFLUXDB_BUCKET \
  -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=$INFLUXDB_TOKEN \
  influxdb:$INFLUXDB_VERSION

# Check if the container is running
if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "InfluxDB container is running successfully."
else
    echo "InfluxDB container failed to start."
    docker logs $CONTAINER_NAME  # Fetch logs to debug why it's not starting
    exit 1
fi

# Print InfluxDB access information
echo ""
echo "InfluxDB setup completed! Access it at http://localhost:8086"
echo ""
echo "InfluxDB credentials:"
echo "--------------------------------"
echo "Username: $INFLUXDB_USER"
echo "Password: $INFLUXDB_PASSWORD"
echo "Organization: $INFLUXDB_ORG"
echo "Bucket: $INFLUXDB_BUCKET"
echo "INFLUXDB_TOKEN: $INFLUXDB_TOKEN"
echo "--------------------------------"
