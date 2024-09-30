#!/bin/bash

# Function to log informational messages
log_info() {
    echo "[INFO] $1"
}

# Function to log error messages and exit
log_error() {
    echo "[ERROR] $1"
    exit 1
}

# Define script directory and configuration directory (two levels up)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
CONFIG_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")/prometheus_config"

# Configuration variables
ALERTMANAGER_CONTAINER="alertmanager"
ALERTMANAGER_IMAGE="prom/alertmanager:latest"
ALERTMANAGER_PORT="9093"
ALERTMANAGER_CONFIG="$CONFIG_DIR/alertmanager.yml"
PROMETHEUS_CONFIG="$CONFIG_DIR/prometheus.yml"
SYSTEMGUARD_APP_IP=$(hostname -I | cut -d' ' -f1)
SYSTEMGUARD_APP_PORT="5050"
ALERTMANAGER_PORT="9093"
ALERTMANAGER_DATA_DIR="/home/$(whoami)/.database/alertmanager"
DOCKER_NETWORK="flask-prometheus-net"
INIT_ALERTMANAGER_SCRIPT="$SCRIPT_DIR/initialization/init_alertmanager.sh"
SYSTEM_LABEL="systemguard-metrics"
JOB_NAME="localhost"
PROMETHEUS_USERNAME="prometheus_admin"
PROMETHEUS_PASSWORD="prometheus_password"

# Verify that initialization script exists
if [ ! -f "$INIT_ALERTMANAGER_SCRIPT" ]; then
  log_error "Initialization script $INIT_ALERTMANAGER_SCRIPT does not exist."
fi

# Execute the initialization script
bash "$INIT_ALERTMANAGER_SCRIPT"

# Ensure configuration and data directories exist
log_info "Creating necessary directories if they don't exist."
mkdir -p "$CONFIG_DIR" || log_error "Failed to create directory: $CONFIG_DIR"
mkdir -p "$ALERTMANAGER_DATA_DIR" || log_error "Failed to create directory: $ALERTMANAGER_DATA_DIR"

# Generate default alertmanager.yml if it does not exist
if [ ! -f "$ALERTMANAGER_CONFIG" ]; then
    log_info "Generating default alertmanager.yml configuration."
    cat > "$ALERTMANAGER_CONFIG" <<EOL
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
    log_info "Using existing alertmanager.yml configuration file."
fi

# Generate or update prometheus.yml
log_info "Updating prometheus.yml configuration."
cat > "$PROMETHEUS_CONFIG" <<EOL
global:
  external_labels:
    system: $SYSTEM_LABEL

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - $SYSTEMGUARD_APP_IP:$ALERTMANAGER_PORT
      timeout: 5m

rule_files:
  - /etc/prometheus/alert_rules.yml

scrape_configs:
  - job_name: $JOB_NAME
    scrape_interval: $SCRAPING_INTERVAL
    static_configs:
      - targets:
          - $SYSTEMGUARD_APP_IP:$SYSTEMGUARD_APP_PORT
    basic_auth:
      username: $PROMETHEUS_USERNAME
      password: $PROMETHEUS_PASSWORD
EOL

# Check if Docker network exists, create if necessary
if ! docker network ls | grep -q "$DOCKER_NETWORK"; then
    log_info "Creating Docker network: $DOCKER_NETWORK"
    docker network create "$DOCKER_NETWORK" || log_error "Failed to create Docker network."
else
    log_info "Docker network $DOCKER_NETWORK already exists."
fi

# Stop and remove existing Alertmanager container if it's running
if docker ps -a --format '{{.Names}}' | grep -q "$ALERTMANAGER_CONTAINER"; then
    log_info "Stopping and removing existing Alertmanager container."
    docker stop "$ALERTMANAGER_CONTAINER" &> /dev/null || log_error "Failed to stop container."
    docker rm "$ALERTMANAGER_CONTAINER" &> /dev/null || log_error "Failed to remove container."
else
    log_info "No existing Alertmanager container found."
fi

# Start the Alertmanager container
log_info "Starting Alertmanager container: $ALERTMANAGER_CONTAINER"
run_output=$(docker run -d \
    --name "$ALERTMANAGER_CONTAINER" \
    --network "$DOCKER_NETWORK" \
    -p "$ALERTMANAGER_PORT:9093" \
    --restart always \
    -v "$ALERTMANAGER_CONFIG:/etc/alertmanager/alertmanager.yml" \
    -v "$ALERTMANAGER_DATA_DIR:/alertmanager" \
    "$ALERTMANAGER_IMAGE" 2>&1)

# Verify if the container started successfully
if [ $? -eq 0 ]; then
    log_info "Alertmanager container started successfully on port $ALERTMANAGER_PORT."
    log_info "Alertmanager config file located at $ALERTMANAGER_CONFIG"
else
    log_error "Failed to start Alertmanager container: $run_output"
fi
