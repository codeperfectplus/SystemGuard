#!/bin/bash

# Function to log messages
log() {
    echo "[INFO] $1"
}

# Error handling
error_exit() {
    echo "[ERROR] $1"
    exit 1
}

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# 2 directories up
CONFIG_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"/prometheus_config
# Configuration variables
ALERTMANAGER_CONTAINER_NAME="alertmanager"
ALERTMANAGER_IMAGE="prom/alertmanager:latest"
ALERTMANAGER_PORT="9093"
ALERTMANAGER_CONFIG_FILE="$CONFIG_DIR/alertmanager.yml"
echo $ALERTMANAGER_CONFIG_FILE
ALERTMANAGER_DATA_DIR="/home/$(whoami)/.database/alertmanager"
NETWORK_NAME="flask-prometheus-net"
INIT_ALERTMANAGER_SH="$SCRIPT_DIR/initialization/init_alertmanager.sh"

# Verify the script exists
if [ ! -f "$INIT_ALERTMANAGER_SH" ]; then
  echo "Script $INIT_ALERTMANAGER_SH does not exist."
  exit 1
fi

call INIT_ALERTMANAGER_SH
bash $INIT_ALERTMANAGER_SH

Ensure config and data directories exist
log "Creating necessary directories if they don't exist."
mkdir -p "$CONFIG_DIR" || error_exit "Failed to create $CONFIG_DIR"
mkdir -p "$ALERTMANAGER_DATA_DIR" || error_exit "Failed to create $ALERTMANAGER_DATA_DIR"

# Sample configuration for alertmanager.yml
if [ ! -f "$ALERTMANAGER_CONFIG_FILE" ]; then
    log "Generating default alertmanager.yml configuration file."
    cat > "$ALERTMANAGER_CONFIG_FILE" <<EOL
global:
  resolve_timeout: 5m

route:
  receiver: 'default'

receivers:
  - name: 'default'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
EOL
else
    log "Using existing alertmanager.yml configuration file."
fi

# Check if Docker network exists
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    log "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME" || error_exit "Failed to create Docker network."
else
    log "Docker network $NETWORK_NAME already exists."
fi

# Stop and remove existing container if it's running
if docker ps -a --format '{{.Names}}' | grep -q "$ALERTMANAGER_CONTAINER_NAME"; then
    log "Stopping and removing existing Alertmanager container."
    docker stop "$ALERTMANAGER_CONTAINER_NAME" &> /dev/null || error_exit "Failed to stop container."
    docker rm "$ALERTMANAGER_CONTAINER_NAME" &> /dev/null || error_exit "Failed to remove container."
else
    log "No existing Alertmanager container found. Proceeding to start a new one."
fi

# Run Alertmanager container
log "Starting Alertmanager container: $ALERTMANAGER_CONTAINER_NAME"
run_output=$(docker run -d \
    --name "$ALERTMANAGER_CONTAINER_NAME" \
    --network "$NETWORK_NAME" \
    -p "$ALERTMANAGER_PORT:9093" \
    --restart always \
    -v "$ALERTMANAGER_CONFIG_FILE:/etc/alertmanager/alertmanager.yml" \
    -v "$ALERTMANAGER_DATA_DIR:/alertmanager" \
    "$ALERTMANAGER_IMAGE" 2>&1)

# Check if Alertmanager started successfully
if [ $? -eq 0 ]; then
    log "Alertmanager container started successfully on port $ALERTMANAGER_PORT."
    log "Alertmanager config file located at $ALERTMANAGER_CONFIG_FILE"
else
    error_exit "Failed to start Alertmanager container: $run_output"
fi
