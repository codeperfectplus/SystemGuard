#!/bin/bash

# Configuration
CONTAINER_NAME="prometheus"
PROMETHEUS_CONFIG="$(pwd)/prometheus.yml"
PROMETHEUS_IMAGE="prom/prometheus"  # Add your image name if needed
NETWORK_NAME="flask-prometheus-net"  # Specify your network name
PROMETHEUS_PORT="9090"  # Specify your port

# Logging function for better readability
log() {
    echo "[INFO] $1"
}

# Check if Prometheus container is running
if [ "$(docker ps -q -f name="$CONTAINER_NAME")" ]; then
    log "Stopping container: $CONTAINER_NAME"
    docker stop "$CONTAINER_NAME"

    log "Starting container: $CONTAINER_NAME with new configuration"
    docker start "$CONTAINER_NAME"

    log "Reloading configuration for container: $CONTAINER_NAME"
    docker exec "$CONTAINER_NAME" kill -HUP 1  # Send SIGHUP to reload config
else
    log "Container $CONTAINER_NAME is not running. Starting a new container."
    docker run -d \
      --name "$CONTAINER_NAME" \
      --network "$NETWORK_NAME" \
      -p "$PROMETHEUS_PORT:$PROMETHEUS_PORT" \
      --restart unless-stopped \
      -v "$PROMETHEUS_CONFIG:/etc/prometheus/prometheus.yml" \
      "$PROMETHEUS_IMAGE" &> /dev/null

    log "Prometheus container started successfully."
fi

log "Prometheus container has been updated with the new configuration."
