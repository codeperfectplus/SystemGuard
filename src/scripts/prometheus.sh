#!/bin/bash

# function to get the user name
get_user_name() {
    if [ "$(whoami)" = "root" ]; then
        LOGNAME_USER=$(logname 2>/dev/null) # Redirect any error output to /dev/null
        if [ $? -ne 0 ]; then               # Check if the exit status of the last command is not 0
            USER_NAME=$(cat /etc/passwd | grep '/home' | cut -d: -f1 | tail -n 1)
        else
            USER_NAME=$LOGNAME_USER
        fi
    else
        USER_NAME=$(whoami)
    fi
    echo "$USER_NAME"
}

USER_NAME=$(get_user_name)
# Configuration
NETWORK_NAME="flask-prometheus-net"
CONTAINER_NAME="prometheus"
PROMETHEUS_IMAGE="prom/prometheus"
PROMETHEUS_PORT="9090"
PROMETHEUS_CONFIG_DIR="$(pwd)/prometheus_config"
PROMETHEUS_CONFIG_FILE="$PROMETHEUS_CONFIG_DIR/prometheus.yml"
PROMETHEUS_DATA_DIR="/home/$USER_NAME/.database/prometheus"
FLASK_APP_IP=$(hostname -I | cut -d' ' -f1)
FLASK_APP_PORT="5050"
SCRAPING_INTERVAL="10s"
JOB_NAME='systemguard-metrics'

# Logging function for better readability
log() {
    echo "[INFO] $1"
}

# Ensure the config directory exists
log "Creating Prometheus config directory if it doesn't exist."
mkdir -p "$PROMETHEUS_CONFIG_DIR"
mkdir -p "$PROMETHEUS_DATA_DIR"

# Create the prometheus.yml configuration file
log "Generating prometheus.yml configuration file."
cat > "$PROMETHEUS_CONFIG_FILE" <<EOL
scrape_configs:
  - job_name: localhost
    scrape_interval: $SCRAPING_INTERVAL
    static_configs:
    - targets:
      - '$FLASK_APP_IP:$FLASK_APP_PORT'
    basic_auth:
      username: admin
      password: admin

EOL

# Check if Docker network exists
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    log "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME"
else
    log "Docker network $NETWORK_NAME already exists."
fi

# Check if Prometheus container is already running
if docker ps -a --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    log "Container $CONTAINER_NAME already exists. Stopping and removing it."
    docker stop "$CONTAINER_NAME" &> /dev/null
    docker rm "$CONTAINER_NAME" &> /dev/null
else
    log "No existing container found. Proceeding to start a new one."
fi

# Run Prometheus container
log "Starting Prometheus container: $CONTAINER_NAME"
run_output=$(docker run -d \
  --name "$CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -p "$PROMETHEUS_PORT:$PROMETHEUS_PORT" \
  --restart always \
  -v "$PROMETHEUS_CONFIG_FILE:/etc/prometheus/prometheus.yml" \
  -v "PROMETHEUS_DATA_DIR:/prometheus" \
  "$PROMETHEUS_IMAGE" 2>&1)  # Capture both stdout and stderr

# Check if Prometheus started successfully
if [ $? -eq 0 ]; then
    log "Prometheus container $CONTAINER_NAME started successfully on port $PROMETHEUS_PORT."
    log "Prometheus config file located at $PROMETHEUS_CONFIG_FILE"
else
    echo "[ERROR] Failed to start Prometheus container: $run_output"
    echo "[ERROR] Checking logs for container: $CONTAINER_NAME"
    exit 1
fi
