#!/bin/bash

# Configuration
NETWORK_NAME="flask-prometheus-net"
CONTAINER_NAME="prometheus"
PROMETHEUS_IMAGE="prom/prometheus"
PROMETHEUS_PORT="9090"
PROMETHEUS_CONFIG_DIR="$(pwd)/prometheus_config"
PROMETHEUS_CONFIG_FILE="$PROMETHEUS_CONFIG_DIR/prometheus.yml"
FLASK_APP_IP=$(hostname -I | cut -d' ' -f1)
FLASK_APP_PORT="5050"

# Logging function for better readability
log() {
    echo "[INFO] $1"
}

# Ensure the config directory exists
log "Creating Prometheus config directory if it doesn't exist."
mkdir -p "$PROMETHEUS_CONFIG_DIR"

# Create the prometheus.yml configuration file
log "Generating prometheus.yml configuration file."
cat > "$PROMETHEUS_CONFIG_FILE" <<EOL
global:
  scrape_interval: 30s  # How often Prometheus scrapes the target

scrape_configs:
  - job_name: 'flask_app_metrics'  # Scraping metrics from Flask app
    static_configs:  # first ip address in the local machine ip address list
      - targets: ['$FLASK_APP_IP:$FLASK_APP_PORT']
      # apeend more targets list to scrape metrics from multiple services, on central prometheus server
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
fi

# Run Prometheus container
log "Starting Prometheus container: $CONTAINER_NAME"
docker run -d \
  --name "$CONTAINER_NAME" \
  --network "$NETWORK_NAME" \
  -p "$PROMETHEUS_PORT:$PROMETHEUS_PORT" \
  --restart unless-stopped \
  -v "$PROMETHEUS_CONFIG_FILE:/etc/prometheus/prometheus.yml" \
  "$PROMETHEUS_IMAGE" &> /dev/null

# Check if Prometheus started successfully
if [ $? -eq 0 ]; then
    log "Prometheus container $CONTAINER_NAME started successfully on port $PROMETHEUS_PORT."
    log "Prometheus config file located at $PROMETHEUS_CONFIG_FILE"
else
    echo "[ERROR] Failed to start Prometheus container."
    exit 1
fi
