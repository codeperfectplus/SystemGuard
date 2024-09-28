#!/bin/bash

# Function to get the user name
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

USER_NAME=$(get_user_name)

# Configuration
NETWORK_NAME="flask-prometheus-net"
CONTAINER_NAME="prometheus"
PROMETHEUS_IMAGE="prom/prometheus:v2.55.0-rc.0"
PROMETHEUS_PORT="9090"
# SCRIPT_DIR and PWD are different
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PROMETHEUS_CONFIG_DIR="$(pwd)/prometheus_config"
ALERT_RULES_FILE="$PROMETHEUS_CONFIG_DIR/alert_rules.yml"
PROMETHEUS_CONFIG_FILE="$PROMETHEUS_CONFIG_DIR/prometheus.yml"
PROMETHEUS_DATA_DIR="/home/$USER_NAME/.database/prometheus"
INIT_ALERT_MANAGER_SCRIPT="$SCRIPT_DIR/initialization/init_alertmanager.sh"
ALERT_MANAGER_SCRIPT="$SCRIPT_DIR/start_alertmanager.sh"
FLASK_APP_IP=$(hostname -I | cut -d' ' -f1)
FLASK_APP_PORT="5050"
SCRAPING_INTERVAL="10s"
monitor="systemguard-metrics"
environment="production"
job_name="localhost"
prometheus_username="prometheus_admin"
prometheus_password="prometheus_password"

# call INIT_ALERT_MANAGER_SCRIPT
# do you want to install alert manager?
echo "Do you want to install Alert Manager? (y/n)"
read install_alert_manager
if [ "$install_alert_manager" = "y" ]; then
    echo "Initializing Alert Manager $INIT_ALERT_MANAGER_SCRIPT"
    bash $INIT_ALERT_MANAGER_SCRIPT
    echo "Starting Alert Manager $ALERT_MANAGER_SCRIPT"
    bash $ALERT_MANAGER_SCRIPT
else
    echo "Skipping Alert Manager installation"
fi

# Logging function for better readability
log() {
    echo "[INFO] $1"
}

# Error function for failed steps
error_exit() {
    echo "[ERROR] $1"
    exit 1
}

# Ensure config and data directories exist
log "Creating necessary directories if they don't exist."
mkdir -p "$PROMETHEUS_CONFIG_DIR" || error_exit "Failed to create $PROMETHEUS_CONFIG_DIR"
mkdir -p "$PROMETHEUS_DATA_DIR" || error_exit "Failed to create $PROMETHEUS_DATA_DIR"

# Ensure Prometheus data directory has correct permissions
log "Setting permissions for Prometheus data directory."
chmod 777 "$PROMETHEUS_DATA_DIR" || error_exit "Failed to set permissions on $PROMETHEUS_DATA_DIR"

# Create prometheus.yml configuration file
log "Generating prometheus.yml configuration file."
cat > "$PROMETHEUS_CONFIG_FILE" <<EOL
global:
  external_labels:
    system: $monitor

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - $FLASK_APP_IP:9093
      timeout: 5m

rule_files:
  - /etc/prometheus/alert_rules.yml

scrape_configs:
  - job_name: $job_name
    scrape_interval: $SCRAPING_INTERVAL
    static_configs:
      - targets:
          - $FLASK_APP_IP:$FLASK_APP_PORT
    basic_auth:
      username: $prometheus_username
      password: $prometheus_password
EOL

# Check if Docker network exists
if ! docker network ls | grep -q "$NETWORK_NAME"; then
    log "Creating Docker network: $NETWORK_NAME"
    docker network create "$NETWORK_NAME" || error_exit "Failed to create Docker network."
else
    log "Docker network $NETWORK_NAME already exists."
fi

# Check if Prometheus container is running, stop and remove if necessary
if docker ps -a --format '{{.Names}}' | grep -q "$CONTAINER_NAME"; then
    log "Stopping and removing existing container: $CONTAINER_NAME."
    docker stop "$CONTAINER_NAME" &> /dev/null || error_exit "Failed to stop container."
    docker rm "$CONTAINER_NAME" &> /dev/null || error_exit "Failed to remove container."
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
  -v "$ALERT_RULES_FILE:/etc/prometheus/alert_rules.yml" \
  -v "$PROMETHEUS_DATA_DIR:/prometheus" \
  "$PROMETHEUS_IMAGE" 2>&1)


# Check if Prometheus started successfully
if [ $? -eq 0 ]; then
    log "Prometheus container $CONTAINER_NAME started successfully on port $PROMETHEUS_PORT."
    log "Prometheus config file located at $PROMETHEUS_CONFIG_FILE"
else
    error_exit "Failed to start Prometheus container: $run_output"
fi
