#!/bin/bash

# Function to determine the username, handles root user case
get_user_name() {
    if [ "$(whoami)" = "root" ]; then
        local logname_user
        logname_user=$(logname 2>/dev/null)
        if [ $? -ne 0 ]; then
            # Fallback: get the last user from /etc/passwd with a home directory
            USER_NAME=$(grep '/home' /etc/passwd | cut -d: -f1 | tail -n 1)
        else
            USER_NAME=$logname_user
        fi
    else
        USER_NAME=$(whoami)
    fi
    echo "$USER_NAME"
}

USER_NAME=$(get_user_name)

# Configuration variables
NETWORK_NAME="flask-prometheus-net"
PROMETHEUS_CONTAINER="prometheus"
PROMETHEUS_IMAGE="prom/prometheus:v2.55.0-rc.0"
PROMETHEUS_PORT="9090"

# Paths and directories
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROMETHEUS_CONFIG_DIR="$(pwd)/prometheus_config"
ALERT_RULES_FILE="$PROMETHEUS_CONFIG_DIR/alert_rules.yml"
PROMETHEUS_CONFIG_FILE="$PROMETHEUS_CONFIG_DIR/prometheus.yml"
PROMETHEUS_DATA_DIR="/home/$USER_NAME/.database/prometheus"
INIT_ALERTMANAGER_SCRIPT="$SCRIPT_DIR/initialization/init_alertmanager.sh"
START_ALERTMANAGER_SCRIPT="$SCRIPT_DIR/start_alertmanager.sh"

# App configuration
FLASK_APP_IP=$(hostname -I | cut -d' ' -f1)
FLASK_APP_PORT="5050"
SCRAPE_INTERVAL="10s"
SYSTEM_LABEL="systemguard-metrics"
ENVIRONMENT="production"
JOB_NAME="localhost"
PROMETHEUS_USERNAME="prometheus_admin"
PROMETHEUS_PASSWORD="prometheus_password"

# Logging function for information
log_info() {
    echo "[INFO] $1"
}

# Error function for failed steps
log_error() {
    echo "[ERROR] $1"
    exit 1
}

# Ensure configuration and data directories exist
log_info "Creating necessary directories if they don't exist."
mkdir -p "$PROMETHEUS_CONFIG_DIR" || log_error "Failed to create directory: $PROMETHEUS_CONFIG_DIR"
mkdir -p "$PROMETHEUS_DATA_DIR" || log_error "Failed to create directory: $PROMETHEUS_DATA_DIR"

# Set correct permissions for the Prometheus data directory
log_info "Setting permissions for Prometheus data directory."
chmod 777 "$PROMETHEUS_DATA_DIR" || log_error "Failed to set permissions on $PROMETHEUS_DATA_DIR"

# Create Prometheus configuration file
log_info "Generating prometheus.yml configuration file."
cat > "$PROMETHEUS_CONFIG_FILE" <<EOL
global:
  external_labels:
    system: $SYSTEM_LABEL

rule_files:
  - /etc/prometheus/alert_rules.yml

scrape_configs:
  - job_name: $JOB_NAME
    scrape_interval: $SCRAPE_INTERVAL
    static_configs:
      - targets:
          - $FLASK_APP_IP:$FLASK_APP_PORT
    basic_auth:
      username: $PROMETHEUS_USERNAME
      password: $PROMETHEUS_PASSWORD
EOL

# Check if Docker network exists, create it if not
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    log_info "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME" || log_error "Failed to create Docker network."
else
    log_info "Docker network $NETWORK_NAME already exists."
fi

# Check if Prometheus container is running, stop and remove it if necessary
if docker ps -a --format '{{.Names}}' | grep -q "$PROMETHEUS_CONTAINER"; then
    log_info "Stopping and removing existing Prometheus container: $PROMETHEUS_CONTAINER."
    docker stop "$PROMETHEUS_CONTAINER" &> /dev/null || log_error "Failed to stop Prometheus container."
    docker rm "$PROMETHEUS_CONTAINER" &> /dev/null || log_error "Failed to remove Prometheus container."
else
    log_info "No existing Prometheus container found. Proceeding to start a new one."
fi

# Start Prometheus container
log_info "Starting Prometheus container: $PROMETHEUS_CONTAINER"
run_output=$(docker run -d \
    --name "$PROMETHEUS_CONTAINER" \
    --network "$NETWORK_NAME" \
    -p "$PROMETHEUS_PORT:$PROMETHEUS_PORT" \
    --restart always \
    -v "$PROMETHEUS_CONFIG_FILE:/etc/prometheus/prometheus.yml" \
    -v "$ALERT_RULES_FILE:/etc/prometheus/alert_rules.yml" \
    -v "$PROMETHEUS_DATA_DIR:/prometheus" \
    "$PROMETHEUS_IMAGE" 2>&1)

# Verify if Prometheus container started successfully
if [ $? -eq 0 ]; then
    log_info "Prometheus container $PROMETHEUS_CONTAINER started successfully on port $PROMETHEUS_PORT."
    log_info "Prometheus config file located at $PROMETHEUS_CONFIG_FILE"
else
    log_error "Failed to start Prometheus container: $run_output"
fi
